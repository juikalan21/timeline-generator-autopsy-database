import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def connect_to_db(db_path):
    conn = sqlite3.connect(db_path)
    return conn

def extract_data(conn):
    query = """
    SELECT 
        datetime(e.ctime, 'unixepoch') as created_time,
        datetime(e.atime, 'unixepoch') as accessed_time,
        datetime(e.mtime, 'unixepoch') as modified_time,
        datetime(e.crtime, 'unixepoch') as changed_time,
        e.name, 
        e.parent_path,
        e.size,
        e.mime_type
    FROM tsk_files as e
    WHERE e.ctime IS NOT NULL OR e.atime IS NOT NULL OR e.mtime IS NOT NULL OR e.crtime IS NOT NULL
    """
    df = pd.read_sql_query(query, conn)
    return df

def generate_timeline(df):
    events = []
    for index, row in df.iterrows():
        if row['created_time']:
            events.append({'time': row['created_time'], 'event': 'Created', 'file': row['name'], 'path': row['parent_path']})
        if row['accessed_time']:
            events.append({'time': row['accessed_time'], 'event': 'Accessed', 'file': row['name'], 'path': row['parent_path']})
        if row['modified_time']:
            events.append({'time': row['modified_time'], 'event': 'Modified', 'file': row['name'], 'path': row['parent_path']})
        if row['changed_time']:
            events.append({'time': row['changed_time'], 'event': 'Changed', 'file': row['name'], 'path': row['parent_path']})

    timeline_df = pd.DataFrame(events)
    timeline_df['time'] = pd.to_datetime(timeline_df['time'])
    timeline_df = timeline_df.sort_values(by='time')
    return timeline_df

def plot_timeline(timeline_df):
    plt.figure(figsize=(10, 6))
    plt.plot(timeline_df['time'], timeline_df['event'], 'o')
    plt.xlabel('Time')
    plt.ylabel('Event')
    plt.title('Timeline Analysis')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    db_path = r'C:\Users\juika\OneDrive\Desktop\GPCSSI_PROJECT\TIMELINE GENERATOR FOR AUTOPSY DATABASE\autopsy.db'

    conn = connect_to_db(db_path)
    df = extract_data(conn)
    timeline_df = generate_timeline(df)
    plot_timeline(timeline_df)
    conn.close()

if __name__ == '__main__':
    main()
