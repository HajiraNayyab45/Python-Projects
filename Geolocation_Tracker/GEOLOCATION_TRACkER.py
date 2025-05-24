import requests
import folium
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

def get_geolocation(ip_address=""):
    """
    Fetch geolocation data for the given IP address.
    If no IP address is provided, it fetches the geolocation of the current user.
    """
    try:
        # Use ip-api.com to fetch geolocation data
        url = f"http://ip-api.com/json/{ip_address}"
        response = requests.get(url)
        data = response.json()
        
        if data['status'] == 'success':
            return {
                "latitude": data['lat'],
                "longitude": data['lon'],
                "city": data['city'],
                "region": data['regionName'],
                "country": data['country'],
                "ip": data['query']
            }
        else:
            messagebox.showerror("Error", f"API Error: {data['message']}")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None

def display_location_on_map(location_data):
    """
    Display the geolocation on a map using folium and open it in the browser.
    """
    try:
        # Extract latitude and longitude
        latitude = location_data['latitude']
        longitude = location_data['longitude']
        city = location_data['city']
        country = location_data['country']
        
        # Create a map centered at the location
        map_object = folium.Map(location=[latitude, longitude], zoom_start=12)
        
        # Add a marker with location details
        folium.Marker(
            [latitude, longitude],
            popup=f"{city}, {country}",
            tooltip="Click for more info"
        ).add_to(map_object)
        
        # Save the map as an HTML file
        map_file = "geolocation_map.html"
        map_object.save(map_file)
        
        # Open the map in the default web browser
        webbrowser.open(map_file)
        messagebox.showinfo("Success", f"Map has been saved as {map_file} and opened in your browser.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while displaying the map: {e}")

def fetch_and_display():
    """
    Fetch geolocation data and display it on a map and in the GUI.
    """
    ip_address = ip_entry.get().strip()
    location_data = get_geolocation(ip_address)
    
    if location_data:
        # Display geolocation data
        data_text.set(f"Geolocation Data:\n{location_data}")
        
        # Display the location on the map
        display_location_on_map(location_data)

# Create the GUI
root = tk.Tk()
root.title("Geolocation Tracker")
root.geometry("800x600")

# Style the GUI
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12))

# Input field for IP address
ttk.Label(root, text="Enter IP Address (leave blank for your own IP):").pack(pady=5)
ip_entry = ttk.Entry(root, width=40)
ip_entry.pack(pady=5)

# Button to fetch and display geolocation
fetch_button = ttk.Button(root, text="Fetch Location", command=fetch_and_display)
fetch_button.pack(pady=10)

# Label to display geolocation data
data_text = tk.StringVar()
data_label = ttk.Label(root, textvariable=data_text, wraplength=600, justify="left")
data_label.pack(pady=10)

# Exit button
exit_button = ttk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=10)

# Run the GUI event loop
root.mainloop()