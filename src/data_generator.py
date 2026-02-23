import pandas as pd
import numpy as np
import random

np.random.seed(42)

roles = {
    "Employee": {"download": (20, 100), "files": (5, 25)},
    "Developer": {"download": (50, 200), "files": (10, 40)},
    "Finance": {"download": (30, 150), "files": (8, 30)},
    "Admin": {"download": (100, 400), "files": (20, 60)},
    "Executive": {"download": (10, 80), "files": (5, 20)}
}

data = []

for i in range(2000):
    role = random.choice(list(roles.keys()))
    login_hour = np.clip(np.random.normal(10, 2), 0, 23)
    files_accessed = np.random.randint(*roles[role]["files"])
    data_downloaded = np.random.randint(*roles[role]["download"])
    failed_logins = np.random.randint(0, 4)
    usb_activity = np.random.choice([0,1], p=[0.9,0.1])
    weekend_activity = np.random.choice([0,1], p=[0.85,0.15])
    after_hours = 1 if login_hour < 6 or login_hour > 20 else 0

    data.append([
        role,
        login_hour,
        files_accessed,
        data_downloaded,
        failed_logins,
        usb_activity,
        weekend_activity,
        after_hours
    ])

df = pd.DataFrame(data, columns=[
    "role",
    "login_hour",
    "files_accessed",
    "data_downloaded_MB",
    "failed_logins",
    "usb_activity",
    "weekend_activity",
    "after_hours_activity"
])

df.to_csv("../data/enterprise_employee_logs.csv", index=False)
print("Enterprise dataset generated.")
