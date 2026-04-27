import numpy as np
import pandas as pd
import math


class IMUIntegrator:
    def __init__(self, csv_path="data/imu_output.csv", output_path="data/imu_integration.csv"):
        self.csv_path = csv_path
        self.output_path = output_path

        # Load input CSV
        self.df = pd.read_csv(csv_path)

        n = len(self.df)
        self.position = np.zeros((n, 2))  # px, py
        self.velocity = np.zeros((n, 2))  # vx, vy
        self.heading = np.zeros(n)        # heading in degrees

        # High-pass filter buffers
        self.ax_hp = np.zeros(n)
        self.ay_hp = np.zeros(n)
        self.az_hp = np.zeros(n)
        self.gz_hp = np.zeros(n)

        # HPF smoothing factors
        self.alpha_accel = 0.98
        self.alpha_gyro = 0.98

    def high_pass(self, x, y_prev, x_prev, alpha):
        """One-step high-pass filter."""
        return alpha * (y_prev + x - x_prev)

    def process(self):
        timestamps = self.df['timestamp_us'].values

        # Initial heading = 0 degrees
        self.heading[0] = 0.0

        # Initialize HPF previous values
        prev_ax = self.df.at[0, 'ax']
        prev_ay = self.df.at[0, 'ay']
        prev_az = self.df.at[0, 'az']
        prev_gz = self.df.at[0, 'gz']

        for i in range(1, len(self.df)):
            dt = timestamps[i] - timestamps[i - 1]

            # Reject bad dt values
            if dt <= 0 or dt > 1:
                dt = 0.01  # assume 100 Hz fallback

            # -----------------------------
            # 1. Raw sensor readings
            # -----------------------------
            ax_raw = self.df.at[i, 'ax']
            ay_raw = self.df.at[i, 'ay']
            az_raw = self.df.at[i, 'az']
            gz_raw = self.df.at[i, 'gz']

            # -----------------------------
            # 2. High-pass filter accel + gyro
            # -----------------------------
            self.ax_hp[i] = self.high_pass(ax_raw, self.ax_hp[i-1], prev_ax, self.alpha_accel)
            self.ay_hp[i] = self.high_pass(ay_raw, self.ay_hp[i-1], prev_ay, self.alpha_accel)
            self.az_hp[i] = self.high_pass(az_raw, self.az_hp[i-1], prev_az, self.alpha_accel)
            self.gz_hp[i] = self.high_pass(gz_raw, self.gz_hp[i-1], prev_gz, self.alpha_gyro)

            # Update previous raw values
            prev_ax, prev_ay, prev_az, prev_gz = ax_raw, ay_raw, az_raw, gz_raw

            # -----------------------------
            # 3. Integrate heading from HPF gyro
            # -----------------------------
            self.heading[i] = self.heading[i-1] + math.degrees(self.gz_hp[i] * dt)
            self.heading[i] = (self.heading[i] + 360) % 360

            heading_rad = math.radians(self.heading[i])

            # -----------------------------
            # 4. Remove gravity (after HPF)
            # -----------------------------
            az_no_gravity = self.az_hp[i] - 9.80665

            # -----------------------------
            # 5. Rotate accel into world frame
            # -----------------------------
            cos_h = math.cos(heading_rad)
            sin_h = math.sin(heading_rad)

            ax_w = self.ax_hp[i] * cos_h - self.ay_hp[i] * sin_h
            ay_w = self.ax_hp[i] * sin_h + self.ay_hp[i] * cos_h

            # -----------------------------
            # 6. Integrate velocity
            # -----------------------------
            self.velocity[i, 0] = self.velocity[i-1, 0] + ax_w * dt
            self.velocity[i, 1] = self.velocity[i-1, 1] + ay_w * dt

            # -----------------------------
            # 7. Integrate position
            # -----------------------------
            self.position[i, 0] = self.position[i-1, 0] + self.velocity[i, 0] * dt
            self.position[i, 1] = self.position[i-1, 1] + self.velocity[i, 1] * dt

        # Build output DataFrame
        self.result = self.df.copy()
        self.result["vx"] = self.velocity[:, 0]
        self.result["vy"] = self.velocity[:, 1]
        self.result["px"] = self.position[:, 0]
        self.result["py"] = self.position[:, 1]
        self.result["heading_deg"] = self.heading

        # Save to CSV
        self.result.to_csv(self.output_path, index=False)
        print(f"Saved processed dataset to {self.output_path}")

        return self.result

    
    def location_from_time(self, time): 

        # index of integrated data at the time we're looking for
        exact_index = self.result.index[self.result['timestamp_us']==time].tolist()

        if len(exact_index) > 0:      # we found an exact match for the time

            px = self.result.iloc[exact_index[0]]['px']
            py = self.result.iloc[exact_index[0]]['py']
            heading = self.result.iloc[exact_index[0]]['heading_deg']

            return px, py, heading
        
        # look for the closest times and interpolate approximate position
        else:
            #iterate through rows of dataframe
            for i, row in self.result.iterrows():
                # pass if before the time we want
                if row['timestamp_us'] < time:
                    pass
                # once we get to time after the one we're searching for
                else:
                    # get data directly before and after the time we want
                    before_row = self.result.iloc[i-1]
                    after_row = self.result.iloc[i]
                    # math to figure out position in between
                    between_ratio = (time-before_row['timestamp_us'])/(after_row['timestamp_us'] - before_row['timestamp_us'])
                    # get positon in between times
                    px = between_ratio * (after_row['px'] - before_row['px']) + before_row['px']
                    py = between_ratio * (after_row['py'] - before_row['py']) + before_row['py']
                    heading = between_ratio * (after_row['heading_deg'] - before_row['heading_deg']) + before_row['heading_deg']

                    return px, py, heading

''' how to use (second line needed)

imu = IMUIntegrator("imu_output.csv", "imu_integration.csv")
result_df = imu.process()
px, py, heading = imu.location_from_time(1234567890)

'''
