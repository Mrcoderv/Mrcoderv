"""
Date utility functions for Nepali calendar conversion
Integrates with the existing date converter code
"""

from datetime import datetime, timedelta

class DateConverter:
    """Convert between BS (Bikram Sambat) and AD (Anno Domini) dates"""
    
    @staticmethod
    def bs_to_ad(bs_year, bs_month, bs_day):
        """
        Convert Bikram Sambat date to Anno Domini date
        Note: This is a simplified conversion for demonstration
        Real implementation would need accurate calendar mapping
        """
        # Simplified conversion (the existing C code logic)
        ad_year = bs_year - 56
        ad_month = bs_month - 8
        ad_day = bs_day - 17
        
        # Handle day overflow
        if ad_day <= 0:
            ad_day += 30
            ad_month -= 1
        
        # Handle month overflow
        if ad_month <= 0:
            ad_month += 12
            ad_year -= 1
        
        return ad_year, ad_month, ad_day
    
    @staticmethod
    def ad_to_bs(ad_year, ad_month, ad_day):
        """
        Convert Anno Domini date to Bikram Sambat date
        Note: This is a simplified conversion for demonstration
        """
        # Simplified conversion (the existing C code logic)
        bs_year = ad_year + 56
        bs_month = ad_month + 8
        bs_day = ad_day + 17
        
        # Handle day overflow
        if bs_day > 30:
            bs_day -= 30
            bs_month += 1
        
        # Handle month overflow
        if bs_month > 12:
            bs_month -= 12
            bs_year += 1
        
        return bs_year, bs_month, bs_day
    
    @staticmethod
    def get_current_bs_date():
        """Get current date in Bikram Sambat"""
        now = datetime.now()
        return DateConverter.ad_to_bs(now.year, now.month, now.day)
    
    @staticmethod
    def format_bs_date(bs_year, bs_month, bs_day):
        """Format BS date as string"""
        return f"{bs_year:04d}-{bs_month:02d}-{bs_day:02d}"
    
    @staticmethod
    def format_ad_date(ad_year, ad_month, ad_day):
        """Format AD date as string"""
        return f"{ad_year:04d}-{ad_month:02d}-{ad_day:02d}"

class NepaliDateUtils:
    """Utility functions for working with Nepali dates in stock market context"""
    
    NEPALI_MONTHS = [
        "बैशाख", "जेठ", "आषाढ", "श्रावण", "भाद्र", "आश्विन",
        "कार्तिक", "मंसिर", "पौष", "माघ", "फाल्गुन", "चैत्र"
    ]
    
    ENGLISH_MONTHS = [
        "Baisakh", "Jestha", "Ashadh", "Shrawan", "Bhadra", "Ashwin",
        "Kartik", "Mangsir", "Poush", "Magh", "Falgun", "Chaitra"
    ]
    
    @staticmethod
    def get_nepali_month_name(month_num, language='english'):
        """Get Nepali month name"""
        if language == 'nepali':
            return NepaliDateUtils.NEPALI_MONTHS[month_num - 1]
        else:
            return NepaliDateUtils.ENGLISH_MONTHS[month_num - 1]
    
    @staticmethod
    def is_trading_day(date):
        """
        Check if a given date is a trading day in Nepal
        (excluding weekends and holidays)
        """
        # In Nepal, Saturday is a holiday, Sunday-Friday are working days
        weekday = date.weekday()
        return weekday != 5  # Saturday is weekday 5
    
    @staticmethod
    def get_trading_days_in_range(start_date, end_date):
        """Get list of trading days between two dates"""
        trading_days = []
        current_date = start_date
        
        while current_date <= end_date:
            if NepaliDateUtils.is_trading_day(current_date):
                trading_days.append(current_date)
            current_date += timedelta(days=1)
        
        return trading_days
    
    @staticmethod
    def get_nepali_fiscal_year(date=None):
        """
        Get Nepali fiscal year for a given date
        Nepali fiscal year starts from Shrawan (roughly mid-July)
        """
        if date is None:
            date = datetime.now()
        
        bs_year, bs_month, bs_day = DateConverter.ad_to_bs(date.year, date.month, date.day)
        
        # If month is Shrawan (4) or later, it's the same fiscal year
        # Otherwise, it's the previous fiscal year
        if bs_month >= 4:
            fiscal_year = bs_year
        else:
            fiscal_year = bs_year - 1
        
        return f"{fiscal_year:04d}/{(fiscal_year + 1) % 100:02d}"