from .login_controller import get_db_connection


# Check Conflict 
def check_schedule_conflict(room, target_date, start_time, end_time):
    conn = get_db_connection()
    if not conn:
        return True 

    try:
        cursor = conn.cursor()
        
        sql = """
        SELECT 1 FROM Sessions 
        WHERE room = %s AND date = %s 
        AND NOT (end_time <= %s OR start_time >= %s)
        """
        cursor.execute(sql, (room, target_date, end_time, start_time))
        
        if cursor.fetchone():
            return True 
        return False    

    except Exception as e:
        print("Schedule Check Error:", e)
        return True
    finally:
        if conn.is_connected():
            conn.close()


# Save Schedule 

def save_new_schedule(class_id, target_date, start_time, end_time, room):
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        
        sql = """
        INSERT INTO Sessions (class_id, date, start_time, end_time, room) 
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (class_id, target_date, start_time, end_time, room))
        conn.commit()
        return True
        
    except Exception as e:
        print("Save Schedule Error:", e)
        return False
    finally:
        if conn.is_connected():
            conn.close()
