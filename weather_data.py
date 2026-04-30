import os
import pandas as pd
import requests
from datetime import datetime, timedelta
import time

def comprehensive_weather_download_2000_2023():
    """
    Download comprehensive weather data for India (2000-2023)
    """
    
    # Create directories
    os.makedirs('weather_dataset/weather_2000_2023', exist_ok=True)
    
    # Define Indian regions with coordinates
    indian_regions = {
    "Uttar Pradesh": (26.8467, 80.9462),
    "Maharashtra": (19.0760, 72.8777),
    "Tamil Nadu": (13.0827, 80.2707),
    "Delhi": (28.6139, 77.2090),
    "West Bengal": (22.5726, 88.3639),
    "Karnataka": (12.9716, 77.5946),
    "Gujarat": (23.0225, 72.5714),
    "Rajasthan": (26.9124, 75.7873),
    "Bihar": (25.5941, 85.1376),
    "Kerala": (8.5241, 76.9366),
    "Punjab": (30.7333, 76.7794),
    "Assam": (26.1445, 91.7362),
    "Jharkhand": (23.6102, 85.2799),
    "Odisha": (20.2961, 85.8245),
    "Chhattisgarh": (21.2514, 81.6296),
    "Haryana": (29.0588, 76.0856),
    "Madhya Pradesh": (23.2599, 77.4126),
    "Andhra Pradesh": (16.5062, 80.6480),
    "Telangana": (17.3850, 78.4867),
    "Uttarakhand": (30.3165, 78.0322),
    "Himachal Pradesh": (31.1048, 77.1734),
    "Goa": (15.2993, 74.1240),
    "Tripura": (23.8315, 91.2868),
    "Manipur": (24.8170, 93.9368),
    "Meghalaya": (25.5788, 91.8933),
    "Nagaland": (26.1584, 94.5624),
    "Mizoram": (23.1645, 92.9376),
    "Arunachal Pradesh": (27.1000, 93.6167),
    "Sikkim": (27.5330, 88.5122),
    "Puducherry": (11.9139, 79.8145),
    "Jammu and Kashmir": (34.0837, 74.7973),
    "Ladakh": (34.1526, 77.5770),
    "Andaman and Nicobar Islands": (11.7401, 92.6586),

    # Newly separated UTs
    "Dadra and Nagar Haveli": (20.1809, 73.0169),
    "Daman and Diu": (20.4283, 72.8397),

    # Newly added
    "Chandigarh": (30.7333, 76.7794)
}

    print("=== Downloading Weather Data (2000-2023) ===")
    
    successful_downloads = 0
    failed_downloads = 0
    
    for city, (lat, lon) in indian_regions.items():
        try:
            print(f"\nDownloading data for {city}...")
            
            # NASA POWER API call
            url = "https://power.larc.nasa.gov/api/temporal/daily/point"
            
            params = {
                'start': '20000101',
                'end': '20231231',  # Up to current available data
                'latitude': lat,
                'longitude': lon,
                'community': 'AG',
                'parameters': 'T2M,T2M_MIN,T2M_MAX,PRECTOTCORR,RH2M,WS2M,ALLSKY_SFC_SW_DWN,PS',
                'format': 'JSON'
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'properties' in data:
                    # Convert to DataFrame
                    df = pd.DataFrame(data['properties']['parameter'])
                    df.index = pd.to_datetime(df.index)
                    
                    # Add location info
                    df['city'] = city
                    df['latitude'] = lat
                    df['longitude'] = lon
                    
                    # Save to CSV
                    filename = f'weather_dataset/weather_2000_2023/weather_{city}_2000_2023.csv'
                    df.to_csv(filename)
                    
                    print(f"   Success: {len(df)} records saved")
                    print(f"   Date range: {df.index.min()} to {df.index.max()}")
                    
                    successful_downloads += 1
                else:
                    print(f" No data in response for {city}")
                    failed_downloads += 1
            else:
                print(f"   HTTP Error {response.status_code} for {city}")
                failed_downloads += 1
                
            # Rate limiting - be respectful to NASA servers
            time.sleep(1)
            
        except Exception as e:
            print(f"   Error downloading {city}: {e}")
            failed_downloads += 1
            continue
    
    print(f"\n=== Download Summary ===")
    print(f"Successful downloads: {successful_downloads}")
    print(f"Failed downloads: {failed_downloads}")
    print(f"Total cities attempted: {len(indian_regions)}")
    
    # Combine all city data into master file
    if successful_downloads > 0:
        os.makedirs('weather_dataset/weather_2000_2023', exist_ok=True)
        combine_weather_files()
    
    return True

def combine_weather_files():
    """Combine all individual weather files into master dataset"""
    
    print("\nCombining all weather files...")
    
    weather_files = []
    data_dir = 'weather_dataset/weather_2000_2023'
    
    for file in os.listdir(data_dir):
        if file.endswith('.csv') and 'weather_' in file:
            df = pd.read_csv(os.path.join(data_dir, file), index_col=0)
            weather_files.append(df)
    
    if weather_files:
        master_df = pd.concat(weather_files, ignore_index=False)
        master_df.to_csv('weather_dataset/weather_2000_2023/master_weather_india_2000_2023.csv')
        
        print(f"Master file created: {len(master_df)} total records")
        print(f"Cities covered: {master_df['city'].nunique()}")
        print(f"Date range: {master_df.index.min()} to {master_df.index.max()}")

# Parameter descriptions for your reference
weather_parameters = {
    'T2M': 'Temperature at 2 Meters (°C)',
    'T2M_MIN': 'Minimum Temperature at 2 Meters (°C)', 
    'T2M_MAX': 'Maximum Temperature at 2 Meters (°C)',
    'PRECTOTCORR': 'Precipitation Corrected (mm/day)',
    'RH2M': 'Relative Humidity at 2 Meters (%)',
    'WS2M': 'Wind Speed at 2 Meters (m/s)',
    'ALLSKY_SFC_SW_DWN': 'All Sky Surface Shortwave Downward Irradiance (kW-hr/m²/day)',
    'PS': 'Surface Pressure (kPa)'
}

# Run the download
if __name__ == "__main__":
    print("Weather Parameters to be downloaded:")
    for param, desc in weather_parameters.items():
        print(f"   {param}: {desc}")
    
    comprehensive_weather_download_2000_2023()