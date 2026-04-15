from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Transfer data from ticket_scenicspot_copy1 to ticket_scenicspot after clearing ticket_scenicspot'

    def handle(self, *args, **options):
        # 清除ticket_scenicspot表中的所有数据
        with connection.cursor() as cursor:
            # 先检查ticket_scenicspot_copy1表是否存在
            cursor.execute("SHOW TABLES LIKE 'ticket_scenicspot_copy1'")
            if not cursor.fetchone():
                self.stdout.write(self.style.ERROR('Error: ticket_scenicspot_copy1 table does not exist'))
                return
            
            # 清除ticket_scenicspot表中的数据
            cursor.execute("DELETE FROM ticket_scenicspot")
            self.stdout.write('Cleared data from ticket_scenicspot table')
            
            # 从ticket_scenicspot_copy1复制数据到ticket_scenicspot
            cursor.execute("""
                INSERT INTO ticket_scenicspot (
                    display_id, admin_id, category, name, description, price, image, 
                    address, opening_hours, is_hot, region_id, tags, rating, 
                    booking_count, total_tickets, is_active, created_at, updated_at
                )
                SELECT 
                    display_id, admin_id, category, name, description, price, image, 
                    address, opening_hours, is_hot, region_id, tags, rating, 
                    booking_count, total_tickets, is_active, created_at, updated_at
                FROM ticket_scenicspot_copy1
            """)
            
            row_count = cursor.rowcount
            self.stdout.write(self.style.SUCCESS(f'Successfully transferred {row_count} rows from ticket_scenicspot_copy1 to ticket_scenicspot'))
