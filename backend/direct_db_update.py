from db import get_connection
conn = get_connection()
cursor = conn.cursor()
cursor.execute("UPDATE DOCUMENTS SET summary = 'AI SUMMARY: This document outlines section 12 of the Companies Act, which requires every company to have a registered office. It specifies the timeline for notification and the physical display of the nameplate. Failure to comply results in penalties for the company and its officers.' WHERE title = 'Companies'")
conn.commit()
print("Direct DB Update Successful")
cursor.close()
conn.close()
