import streamlit as st
import pandas as pd
import json
import plotly.express as px

# Define the path to the JSON file
data_file = 'site_database.json'


# Load data from JSON file if it exists
with open(data_file, 'r') as file:
    data = json.load(file)
st.session_state['data'] = pd.DataFrame(data)

# Set the page title
st.set_page_config(page_title="Site model DataBase", layout="wide")
st.title("Site model DataBase")


#make columns for placments
column_01A, column_01B = st.columns([3, 2])

with column_01A:
    df = st.session_state['data']

    # Create the choropleth map,
    fig = px.scatter_mapbox(df, lat='lat', lon='lon', hover_data=['project_name'], size='radius',
                            zoom=10, height=800, center={'lat':47.609273, 'lon':-122.338963})
    fig.update_layout(mapbox_style="open-street-map")

    # Display the map with selection enabled
    event = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

    # Display selected point information
    if event.selection:
        selected_points = event.selection['points']
        if selected_points:
            index_value = selected_points[0]['point_index']
            current_lat = df.iloc[index_value]['lat']
            current_lon = df.iloc[index_value]['lon']
            current_project_name = df.iloc[index_value]['project_name']
            current_radius = df.iloc[index_value]['radius']
            current_site_link = df.iloc[index_value]['site_link']

            current_options = df.iloc[index_value]['models']
            current_options = [item.strip() for item in current_options.split(",")]

            current_year_modelled = df.iloc[index_value]['year']
            current_description = df.iloc[index_value]['description']
        else:
            current_lat = None
            current_lon = None
            current_project_name = None
            current_radius = None
            current_site_link = None
            current_options = None
            current_year_modelled = None
            current_description = None



with column_01B:
    st.subheader("Site information")
    project_name = st.text_input("Project name", current_project_name, placeholder="what is the name of the project?")

    column_01B1, column_01B2, column_01B3 = st.columns([1, 1, 1])

    with column_01B1:
        lat = st.text_input("Latitiude", current_lat)
    with column_01B2:
        lon = st.text_input("Longitude", current_lon)
    with column_01B3:
        radius = st.text_input("radius(ft)", current_radius)


    site_link = st.text_input("Site link", current_site_link)

    column_01B10, column_01B11 = st.columns([4, 1])
    with column_01B10:
        options = st.multiselect(
            "Models available for",
            ["Rhino3D", "Sketchup", "Revit", "ArcGIS", "N/A"], current_options)
    with column_01B11:
        year_modelled = st.selectbox("year modelled", [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000])


    site_description = st.text_area("Description", current_description, placeholder="Please explain briefly about the site and who are the people to reachout.")


    if st.button("Save Changes"):
        if lat and lon:
            st.session_state['data'] = st.session_state['data'][~((st.session_state['data']['lat'] == float(lat)) & (st.session_state['data']['lon'] == float(lon)))]
            
            # Create new point dictionary
            new_point = {
                'lat': float(lat),
                'lon': float(lon),
                'radius': int(radius) if radius else 25,
                'project_name': project_name if project_name else "N/A",
                'site_link': site_link if site_link else "N/A",
                'models': ', '.join(options) if options else "N/A",
                "year" : year_modelled if year_modelled else "N/A",
                'optiions' : options if options else ["N/A"],
                'description': site_description if site_description else "N/A"
            }
            
            # Append the new point
            st.session_state['data'] = pd.concat([st.session_state['data'], pd.DataFrame([new_point])], ignore_index=True)

            # Save updated data to JSON file
            with open(data_file, 'w') as file:
                json.dump(st.session_state['data'].to_dict(orient='records'), file)

            st.success("Point added! Please refresh to see changes")
        else:
            st.error("Latitude and Longitude are required fields.")


    if st.button("Delete item"):
        if current_lat is not None and current_lon is not None:
            # Delete the selected point and row from df
            st.session_state['data'] = st.session_state['data'][~((st.session_state['data']['lat'] == current_lat) & (st.session_state['data']['lon'] == current_lon))]
            
            # Save updated data to JSON file
            with open(data_file, 'w') as file:
                json.dump(st.session_state['data'].to_dict(orient='records'), file)

            st.success("Point deleted! Please refresh to see changes")
        else:
            st.error("No point selected to delete.")

    if st.button("Refresh"):
        st.rerun()



    

st.write(st.session_state['data'])