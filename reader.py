

from views.data_op.data_loader import load_data

def top_readers(data):
    #checking event type to check if the sample has reading time of a user
    reading_events = data[(data['event_type'] == 'pagereadtime') & (data['subject_type'] == 'doc')]

    #calculating the total time a user spent on readin documents
    total_reading_time = reading_events.groupby('visitor_uuid')['event_readtime'].sum().reset_index()

    #sorting the data in descending order
    total_reading_time = total_reading_time.sort_values(by='event_readtime', ascending=False)

    #returning the top 10 reader based on reading time
    return (total_reading_time["visitor_uuid"].head(10).to_string(index=False))

data = load_data("datasets/dataset.txt")
print(top_readers(data))