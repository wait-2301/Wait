from app.db_connect import db_conn

# Create a cursor to interact with the database
cur = db_conn.cursor()

# Create tables if they don't already exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS public.managers
    (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL UNIQUE,
        added_by BIGINT NOT NULL,
        granted_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        room_id INTEGER
    );
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS public.queue
    (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        queue_number TEXT COLLATE pg_catalog."default" NOT NULL DEFAULT nextval('queue_number_seq'::regclass),
        room_id INTEGER,
        purpose TEXT COLLATE pg_catalog."default" NOT NULL,
        priority BOOLEAN DEFAULT FALSE,
        status TEXT COLLATE pg_catalog."default" DEFAULT 'WAITING',
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        full_name TEXT COLLATE pg_catalog."default"
    );
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS public.queue_history
    (
        id SERIAL PRIMARY KEY,
        "timestamp" TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        user_id BIGINT,
        queue_number VARCHAR(50) COLLATE pg_catalog."default",
        status VARCHAR(50) COLLATE pg_catalog."default",
        client_full_name VARCHAR(255) COLLATE pg_catalog."default",
        manager_id INTEGER
    );
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS public.rooms
    (
        id SERIAL PRIMARY KEY,
        room_name TEXT COLLATE pg_catalog."default" NOT NULL,
        status TEXT COLLATE pg_catalog."default" NOT NULL DEFAULT 'AVAILABLE',
        updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS public.users
    (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL UNIQUE,
        full_name TEXT COLLATE pg_catalog."default" NOT NULL,
        email VARCHAR(255) COLLATE pg_catalog."default",
        passwords VARCHAR COLLATE pg_catalog."default",
        phone_number TEXT COLLATE pg_catalog."default",
        telegram_id BIGINT,
        category TEXT COLLATE pg_catalog."default" DEFAULT 'STANDARD',
        registered_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
''')

# Add foreign key constraints
cur.execute('''
    ALTER TABLE IF EXISTS public.managers
    ADD CONSTRAINT fk_managers_room FOREIGN KEY (room_id)
    REFERENCES public.rooms (id) ON DELETE NO ACTION;
''')

cur.execute('''
    ALTER TABLE IF EXISTS public.queue
    ADD CONSTRAINT fk_queue_room FOREIGN KEY (room_id)
    REFERENCES public.rooms (id) ON DELETE NO ACTION;
''')

cur.execute('''
    ALTER TABLE IF EXISTS public.queue_history
    ADD CONSTRAINT fk_queue_history_manager FOREIGN KEY (manager_id)
    REFERENCES public.managers (id) ON DELETE NO ACTION;
''')

cur.execute('''
    ALTER TABLE IF EXISTS public.users
    ADD CONSTRAINT fk_users_telegram_id FOREIGN KEY (telegram_id)
    REFERENCES public.managers (id) ON DELETE NO ACTION;
''')

# Create the function
cur.execute('''
    CREATE OR REPLACE FUNCTION log_queue_changes()
    RETURNS TRIGGER AS $$
    DECLARE
        manager_id INTEGER;
    BEGIN
        -- Get the manager id associated with the room_id
        SELECT id INTO manager_id 
        FROM managers 
        WHERE room_id = NEW.room_id 
        LIMIT 1;

        -- Insert the new record into queue_history
        INSERT INTO queue_history (
            "timestamp", queue_id, user_id, queue_number, status, full_name, manager_id
        ) 
        VALUES (
            CURRENT_TIMESTAMP, 
            NEW.id, 
            NEW.user_id, 
            NEW.queue_number, 
            NEW.status, 
            NEW.full_name, 
            manager_id
        );

        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
''')

# Create the trigger 
cur.execute('''
    CREATE TRIGGER trigger_log_queue_changes
    AFTER INSERT OR UPDATE ON queue
    FOR EACH ROW 
    EXECUTE FUNCTION log_queue_changes();
''')

#Представление employee_view
cur.execute('''
    CREATE OR REPLACE VIEW public.employee_view AS
SELECT 
    u.user_id AS user_id,
	SPLIT_PART(u.full_name, ' ', 1) AS first_name,
    SPLIT_PART(u.full_name, ' ', 2) AS last_name,
	u.category AS position,
    r.room_name AS table_number,
    u.phone_number AS phone,
    u.passwords AS password_hash
FROM public.users u
JOIN public.managers m ON u.user_id = m.user_id
LEFT JOIN public.rooms r ON m.room_id = r.id;
''')

cur.execute('''
    CREATE OR REPLACE VIEW queue_status_view AS
SELECT 
    jsonb_agg(
        jsonb_build_object(
            'manager', u_manager.full_name,
            'client', q.full_name,
            'status', 
                CASE q.status
                    WHEN 'IN_PROGRESS' THEN 'В ПРОЦЕССЕ'
                    WHEN 'COMPLETED' THEN 'ЗАВЕРШЕН'
                    WHEN 'NO_SHOW' THEN 'НЕЯВКА'
                    ELSE q.status  -- In case there are other status values not mapped
                END,
            'date_time', TO_CHAR(q.created_at, 'YYYY/MM/DD HH24:MI')
        )
    ) AS queue_status_json
FROM 
    queue q
JOIN 
    rooms r ON r.id = q.room_id
JOIN 
    managers m ON m.room_id = r.id
JOIN 
    users u_manager ON u_manager.user_id = m.user_id;
''')


#Index на номер телефона для таблицы users
cur.execute('''
    CREATE INDEX idx_users_phone_number 
    ON public.users (phone_number);
''')



cur.execute('''
    INSERT INTO public.managers(user_id) VALUES (%s), (%s)
''', (5206245464, 1167373997))


db_conn.commit()


cur.execute("SELECT COUNT(*) FROM public.managers;")
managers_count = cur.fetchone()[0]
print("Managers Count in DB: ", managers_count)


cur.close()
db_conn.close()
