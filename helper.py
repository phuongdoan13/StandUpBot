from datetime import datetime, timedelta

class SecondToDesiredHour:
  @staticmethod
  def get_second_until_desired_hour(desired_hour):
    return int((SecondToDesiredHour.__get_datetime_of_next_desired_hour(desired_hour) - datetime.now()).total_seconds())
  
  @staticmethod
  def __get_datetime_of_next_desired_hour(desired_hour):
    datetime_now = datetime.now()
    if(datetime_now.hour >= desired_hour):
      datetime_now += timedelta(days=1)
    return datetime_now.replace(hour=desired_hour, minute=0, second=0, microsecond=0)