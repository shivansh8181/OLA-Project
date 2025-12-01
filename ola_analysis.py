# OLA Bookings Data Analysis Script
# Comprehensive Analysis of 70,000 Booking Records

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

# Set style for visualizations
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

print("="*80)
print(" "*25 + "OLA BOOKINGS DATA ANALYSIS")
print("="*80)

# Load the dataset
print("\n[1/11] Loading dataset...")
df = pd.read_csv('Bookings-70000-Rows.csv')
print(f"✓ Dataset loaded successfully!")
print(f"   Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

# Basic Information
print("\n[2/11] Dataset Overview...")
print("\nFirst 5 rows:")
print(df.head())
print("\nData Types:")
print(df.dtypes)
print("\nBasic Statistics:")
print(df.describe())

# Missing Values Analysis
print("\n[3/11] Missing Values Analysis...")
missing_data = pd.DataFrame({
    'Column': df.columns,
    'Missing_Count': df.isnull().sum(),
    'Missing_Percentage': (df.isnull().sum() / len(df) * 100).round(2)
})
missing_data = missing_data[missing_data['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)
print(missing_data.to_string(index=False))

# Booking Status Analysis
print("\n[4/11] Booking Status Analysis...")
status_counts = df['Booking_Status'].value_counts()
status_pct = (status_counts / len(df) * 100).round(2)
print("\nBooking Status Distribution:")
for status, count in status_counts.items():
    print(f"   {status}: {count:,} ({status_pct[status]}%)")

# Vehicle Type Analysis
print("\n[5/11] Vehicle Type Analysis...")
vehicle_counts = df['Vehicle_Type'].value_counts()
print("\nTop 5 Vehicle Types:")
for vehicle, count in vehicle_counts.head().items():
    print(f"   {vehicle}: {count:,}")

# Success Rate by Vehicle
success_df = df[df['Booking_Status'] == 'Success']
total_by_vehicle = df['Vehicle_Type'].value_counts()
success_by_vehicle = success_df['Vehicle_Type'].value_counts()
success_rate = (success_by_vehicle / total_by_vehicle * 100).round(2).sort_values(ascending=False)
print("\nSuccess Rate by Vehicle Type:")
for vehicle, rate in success_rate.items():
    print(f"   {vehicle}: {rate}%")

# Cancellation Analysis
print("\n[6/11] Cancellation Analysis...")
driver_cancel = df[df['Booking_Status'] == 'Canceled by Driver']['Canceled_Rides_by_Driver'].value_counts()
customer_cancel = df[df['Booking_Status'] == 'Canceled by Customer']['Canceled_Rides_by_Customer'].value_counts()

print("\nTop Driver Cancellation Reasons:")
for reason, count in driver_cancel.head().items():
    print(f"   {reason}: {count:,}")

print("\nTop Customer Cancellation Reasons:")
for reason, count in customer_cancel.head().items():
    print(f"   {reason}: {count:,}")

# Revenue Analysis
print("\n[7/11] Revenue & Payment Analysis...")
total_revenue = success_df['Booking_Value'].sum()
avg_booking_value = success_df['Booking_Value'].mean()
print(f"\nTotal Revenue: ₹{total_revenue:,.2f}")
print(f"Average Booking Value: ₹{avg_booking_value:.2f}")
print(f"Highest Booking: ₹{success_df['Booking_Value'].max():,.2f}")
print(f"Lowest Booking: ₹{success_df['Booking_Value'].min():,.2f}")

# Revenue by Vehicle Type
revenue_by_vehicle = success_df.groupby('Vehicle_Type')['Booking_Value'].sum().sort_values(ascending=False)
print("\nRevenue by Vehicle Type:")
for vehicle, revenue in revenue_by_vehicle.items():
    print(f"   {vehicle}: ₹{revenue:,.2f}")

# Payment Method Distribution
payment_counts = success_df['Payment_Method'].value_counts()
print("\nPayment Method Distribution:")
for method, count in payment_counts.items():
    print(f"   {method}: {count:,}")

# Location Analysis
print("\n[8/11] Location Analysis...")
top_pickups = df['Pickup_Location'].value_counts().head(10)
top_drops = df['Drop_Location'].value_counts().head(10)

print("\nTop 10 Pickup Locations:")
for location, count in top_pickups.items():
    print(f"   {location}: {count:,}")

print("\nTop 10 Drop Locations:")
for location, count in top_drops.items():
    print(f"   {location}: {count:,}")

# Distance Analysis
print("\n[9/11] Ride Distance Analysis...")
print(f"\nAverage Distance: {success_df['Ride_Distance'].mean():.2f} km")
print(f"Median Distance: {success_df['Ride_Distance'].median():.2f} km")
print(f"Max Distance: {success_df['Ride_Distance'].max():.2f} km")
print(f"Total Distance Covered: {success_df['Ride_Distance'].sum():,.2f} km")

avg_distance_by_vehicle = success_df.groupby('Vehicle_Type')['Ride_Distance'].mean().sort_values(ascending=False)
print("\nAverage Distance by Vehicle Type:")
for vehicle, distance in avg_distance_by_vehicle.items():
    print(f"   {vehicle}: {distance:.2f} km")

# Ratings Analysis
print("\n[10/11] Ratings Analysis...")
print(f"\nAverage Driver Rating: {success_df['Driver_Ratings'].mean():.2f}/5.0")
print(f"Average Customer Rating: {success_df['Customer_Rating'].mean():.2f}/5.0")

# TAT Analysis
print("\n[11/11] TAT (Turnaround Time) Analysis...")
print(f"\nAverage Vehicle TAT: {success_df['V_TAT'].mean():.2f} minutes")
print(f"Average Customer TAT: {success_df['C_TAT'].mean():.2f} minutes")

# Executive Summary
print("\n" + "="*80)
print(" "*25 + "EXECUTIVE SUMMARY")
print("="*80)

total_bookings = len(df)
successful_bookings = len(success_df)
canceled_by_driver_count = len(df[df['Booking_Status'] == 'Canceled by Driver'])
canceled_by_customer_count = len(df[df['Booking_Status'] == 'Canceled by Customer'])
driver_not_found_count = len(df[df['Booking_Status'] == 'Driver Not Found'])
success_rate_pct = (successful_bookings / total_bookings * 100)

print(f"\n1. OVERALL PERFORMANCE")
print(f"   Total Bookings: {total_bookings:,}")
print(f"   Successful Bookings: {successful_bookings:,} ({success_rate_pct:.2f}%)")
print(f"   Canceled by Driver: {canceled_by_driver_count:,} ({canceled_by_driver_count/total_bookings*100:.2f}%)")
print(f"   Canceled by Customer: {canceled_by_customer_count:,} ({canceled_by_customer_count/total_bookings*100:.2f}%)")
print(f"   Driver Not Found: {driver_not_found_count:,} ({driver_not_found_count/total_bookings*100:.2f}%)")

print(f"\n2. REVENUE INSIGHTS")
print(f"   Total Revenue: ₹{total_revenue:,.2f}")
print(f"   Average Booking Value: ₹{avg_booking_value:.2f}")

print(f"\n3. VEHICLE INSIGHTS")
most_popular_vehicle = df['Vehicle_Type'].value_counts().index[0]
highest_revenue_vehicle = revenue_by_vehicle.index[0]
print(f"   Most Popular Vehicle: {most_popular_vehicle} ({vehicle_counts[most_popular_vehicle]:,} bookings)")
print(f"   Highest Revenue Vehicle: {highest_revenue_vehicle} (₹{revenue_by_vehicle[highest_revenue_vehicle]:,.2f})")

print(f"\n4. LOCATION INSIGHTS")
print(f"   Most Popular Pickup: {top_pickups.index[0]} ({top_pickups.iloc[0]:,} bookings)")
print(f"   Most Popular Drop: {top_drops.index[0]} ({top_drops.iloc[0]:,} bookings)")
print(f"   Unique Pickup Locations: {df['Pickup_Location'].nunique()}")
print(f"   Unique Drop Locations: {df['Drop_Location'].nunique()}")

print(f"\n5. OPERATIONAL METRICS")
print(f"   Total Distance Covered: {success_df['Ride_Distance'].sum():,.2f} km")
print(f"   Average Ride Distance: {success_df['Ride_Distance'].mean():.2f} km")
print(f"   Average Vehicle TAT: {success_df['V_TAT'].mean():.2f} minutes")
print(f"   Average Customer TAT: {success_df['C_TAT'].mean():.2f} minutes")

print(f"\n6. SERVICE QUALITY")
print(f"   Average Driver Rating: {success_df['Driver_Ratings'].mean():.2f}/5.0")
print(f"   Average Customer Rating: {success_df['Customer_Rating'].mean():.2f}/5.0")

# Key Recommendations
print("\n" + "="*80)
print(" "*25 + "KEY RECOMMENDATIONS")
print("="*80)

recommendations = [
    "\n1. REDUCE CANCELLATIONS:",
    "   • Implement incentives to reduce driver cancellations",
    "   • Address 'Personal & Car related issues' proactively",
    "   • Improve driver-customer matching algorithm",
    "",
    "2. OPTIMIZE PEAK HOURS:",
    "   • Increase driver availability during high-demand hours",
    "   • Implement dynamic pricing during peak times",
    "   • Focus on popular routes for better resource allocation",
    "",
    "3. ENHANCE CUSTOMER EXPERIENCE:",
    "   • Reduce average V_TAT and C_TAT times",
    f"   • Focus on improving driver ratings (current: {success_df['Driver_Ratings'].mean():.2f}/5.0)",
    "   • Address 'Driver not moving towards pickup' complaints",
    "",
    "4. REVENUE OPTIMIZATION:",
    f"   • Focus marketing on {highest_revenue_vehicle} (highest revenue generator)",
    "   • Encourage digital payments with offers",
    "   • Target high-traffic locations for better coverage",
    "",
    "5. OPERATIONAL EFFICIENCY:",
    f"   • Reduce 'Driver Not Found' instances ({driver_not_found_count/total_bookings*100:.1f}% of bookings)",
    "   • Improve vehicle-customer matching based on location data",
    "   • Monitor and reduce incomplete rides",
]

for rec in recommendations:
    print(rec)

print("\n" + "="*80)
print(" "*30 + "ANALYSIS COMPLETE")
print("="*80)

print("\n✓ Analysis completed successfully!")
print(f"✓ Analyzed {total_bookings:,} booking records")
print("✓ Report generated")
