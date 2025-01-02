from webull import webull
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

class WebullTrader:
    def __init__(self):
        load_dotenv()
        self.wb = webull()
        self.setup_logging()
        self.login()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='webull_trader.log'
        )
        self.logger = logging.getLogger(__name__)

    def login(self):
        try:
            self.wb.login(
                username=os.getenv('gardydupiton@gmail.com'),
                password=os.getenv('Reale$tate2023D'),
                device_name='trading_bot'
            )
            self.wb.get_trade_token(os.getenv('157533'))
            self.wb.set_paper_trading()
            self.logger.info("Successfully logged into Webull paper trading")
        except Exception as e:
            self.logger.error(f"Failed to login to Webull: {e}")
            raise

    def place_option_order(self, symbol, option_type, expiry_date, strike_price, quantity):
        try:
            # Get option ID
            option_id = self.wb.get_option_id(
                stock=symbol,
                expireDate=expiry_date,
                strike=strike_price,
                direction=option_type
            )

            # Place paper trading order
            order = self.wb.place_option_order(
                stock=symbol,
                tId=option_id,
                price=0,  # Market order
                quantity=quantity,
                action="BUY",
                orderType="MKT",
                enforce="DAY",
                quoteType="OPTION"
            )
            
            self.logger.info(f"Placed order: {order}")
            return order
        except Exception as e:
            self.logger.error(f"Failed to place option order: {e}")
            return None

    def get_positions(self):
        try:
            return self.wb.get_positions()
        except Exception as e:
            self.logger.error(f"Failed to get positions: {e}")
            return []

    def get_orders(self):
        try:
            return self.wb.get_orders()
        except Exception as e:
            self.logger.error(f"Failed to get orders: {e}")
            return []
