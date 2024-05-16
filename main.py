import datetime
import nepali_datetime
from nepali_datetime import _days_in_month
from nepali_datetime import datetime as ndt
from datetime import datetime as dt

def get_fiscal_year(date_in_string):
    # Convert input date string to date object
    date_obj = datetime.datetime.strptime(date_in_string, "%Y-%m-%d").date()
    
    # Convert Gregorian date to Bikram Sambat (BS) date
    bs_date = nepali_datetime.date.from_datetime_date(date_obj)
    
    # Extract year, month, and day from BS date
    bs_year, bs_month, bs_day = bs_date.year, bs_date.month, bs_date.day
    
    # Calculate fiscal year
    fiscal_year_start_bs = bs_year if bs_month >= 4 else bs_year - 1
    fiscal_year_end_bs = fiscal_year_start_bs + 1
    fiscal_year_short_start_bs = fiscal_year_start_bs % 100
    fiscal_year_short_end_bs = fiscal_year_end_bs % 100
    
    # Calculate fiscal year for Gregorian calendar
    fiscal_year_start_ad = fiscal_year_start_bs - 57
    fiscal_year_end_ad = fiscal_year_end_bs - 57
    fiscal_year_short_start_ad = fiscal_year_start_ad % 100
    fiscal_year_short_end_ad = fiscal_year_end_ad % 100
    
    # Construct fiscal year codes
    short_fiscal_session_bs = f"{fiscal_year_short_start_bs}/{fiscal_year_short_end_bs}"
    short_fiscal_session_ad = f"{fiscal_year_short_start_ad}/{fiscal_year_short_end_ad}"
    full_fiscal_session_ad = f"{fiscal_year_start_ad}/{fiscal_year_end_ad}"
    full_fiscal_session_bs = f"{fiscal_year_start_bs}/{fiscal_year_end_bs}"
    
    # Calculate fiscal year full start and end dates in Bikram Sambat (BS)
    fiscal_year_full_start_date_bs = f"{fiscal_year_start_bs}-04-01"
    fiscal_year_full_end_date_bs = f"{fiscal_year_end_bs}-03-32" if bs_date.year % 4 == 0 else f"{fiscal_year_end_bs}-03-31"

    # Convert fiscal year full start and end dates to Gregorian calendar
    fiscal_year_full_start_date_ad = (date_obj.replace(year=fiscal_year_start_ad) + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    fiscal_year_full_end_date_ad = (date_obj.replace(year=fiscal_year_end_ad) + datetime.timedelta(days=1)).strftime('%Y-%m-%d')


    ad_data = {        
        "current_date_ad": date_in_string,
        "fiscal_year_full_start_date_ad" : fiscal_year_full_start_date_ad,
        "fiscal_year_full_end_date_ad" : fiscal_year_full_end_date_ad,
        "fiscal_year_start_ad": fiscal_year_start_ad,
        "fiscal_year_end_ad": fiscal_year_end_ad,
        "fiscal_year_short_start_ad": fiscal_year_short_start_ad,
        "fiscal_year_short_end_ad": fiscal_year_short_end_ad,
        "short_fiscal_session_ad": short_fiscal_session_ad,
        "full_fiscal_session_ad": full_fiscal_session_ad
    }
    
    bs_data = {
        #9 BS data
        "curr_date_bs": bs_date,
        "fiscal_year_start_bs": fiscal_year_start_bs,
        "fiscal_year_end_bs": fiscal_year_end_bs,
        "fiscal_year_short_start_bs": fiscal_year_short_start_bs,
        "fiscal_year_short_end_bs": fiscal_year_short_end_bs,
        "short_fiscal_session_bs": short_fiscal_session_bs,
        "full_fiscal_session_bs": full_fiscal_session_bs,
        "fiscal_year_full_start_date_bs": fiscal_year_full_start_date_bs,
        "fiscal_year_full_end_date_bs": fiscal_year_full_end_date_bs,
        
    }
    fiscal_calc = {**ad_data, **bs_data}
    return fiscal_calc

## Fiscal Session BS short 80/81
def get_fiscal_year_code_bs():
    return get_fiscal_year(str(dt.now().date()))['short_fiscal_session_bs']

## Fiscal Session BS full 2080/2081
def get_full_fiscal_year_code_bs():
    return get_fiscal_year(str(dt.now().date()))['full_fiscal_session_bs']


## Fiscal Session AD full 23/24
def get_fiscal_year_code_ad():
    return get_fiscal_year(str(dt.now().date()))['short_fiscal_session_ad']

## Fiscal Session AD full 2023/2024
def get_full_fiscal_year_code_ad():
    return get_fiscal_year(str(dt.now().date()))['full_fiscal_session_ad']


def get_quarter_dates_bs(start_year_bs, end_year_bs):
    if end_year_bs != start_year_bs + 1:
        raise ValueError("End year can only be just one year ahead of start year")
    quarter_dates_bs = []
    quarter_dates_bs_ad_conversion = []
    temp_year_bs = start_year_bs
    for quarter in range(1, 5):
        start_month = 3 * (quarter - 1) + 4
        end_month = start_month + 2
        if start_month > 12:
            temp_year_bs = end_year_bs
            start_month = 1
            end_month = 3
        start_date_bs = ndt(temp_year_bs, start_month, 1)
        end_date_bs = ndt(temp_year_bs, end_month, _days_in_month(temp_year_bs, end_month))  # Last day of the month

        start_date_ad_ = ndt.date(start_date_bs)
        start_date_ad = start_date_ad_.to_datetime_date().strftime("%Y-%m-%d")

        end_date_ad_ = ndt.date(end_date_bs)
        end_date_ad = end_date_ad_.to_datetime_date().strftime("%Y-%m-%d")
        
        quarter_dates_bs_ad_conversion.append((start_date_ad, end_date_ad))
        quarter_dates_bs.append((start_date_bs.strftime("%Y-%m-%d"), end_date_bs.strftime("%Y-%m-%d")))
    return quarter_dates_bs_ad_conversion, quarter_dates_bs

def generate_quarter_dates_bs():
    now = str((datetime.datetime.now().date()))
    fiscal_calculation = get_fiscal_year(now)
    
    
    fiscal_start_bs = fiscal_calculation['fiscal_year_start_bs']
    fiscal_end_bs = fiscal_calculation['fiscal_year_end_bs']

    bs_quarter_in_ad, bs_quarter = get_quarter_dates_bs(
        start_year_bs=fiscal_start_bs,
        end_year_bs=fiscal_end_bs
    )
    return bs_quarter_in_ad, bs_quarter



a, b = generate_quarter_dates_bs()