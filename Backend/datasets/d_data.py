import pandas as pd

# Create data for doctors
doctor_names = ["Rahul Mehrotra", "Parveen Yadav", "Sakshi Karkra", "Ravi Sahuta", "Sanjeev Srivastava",
                "Atul Sharma", "Pooja Aggarwal", "M.A Mir", "Biswajyoti Hazarika", "Himangshu Tyagi", 
                "S Jayalakshmi", "Krishna Subramony Iyer", "Shafiq Ahmed", "Saurabh Pokhariyal", "Sanjay Gogoi", 
                "Vedant Kabra", "Devendra Yadav", "T.Krishan Thusoo", "Sandeep Chauhan", "Renu Raina Sehgal", 
                "Smita Vats", "Shashidhar Shree Niwas", "S K Rajan", "Ajit Singh Baghela", "Deepa Maheshwari", "Tapan Singh Chauhan", 
                "Veena Bhat", "Nidhi Jain", "Nutan Agarwal", "Manish Mahajan", "Nitin Kumar Parashar", "Kuldeep Arora", "Sanjay Sarup", 
                "S.V. Kotwal", "Aditya Dixit", "Abhinandan Mukhopadhyay", "Abhinandan Mishra", "Pawan Rawal", "B Kalra", 
                "Asha Sharma", "Pawan Goyal"]
doctor_ratings = [8, 7, 7, 8, 9, 10, 8, 7, 6, 8, 8, 9, 6, 7, 8, 6, 10, 6, 7, 8, 6, 9, 8, 9, 5, 6, 8, 9, 10, 8, 9, 7, 6, 9, 7, 8, 9, 6, 9, 10, 9]
latitudes = [22.563339490187055, 22.573207113591405, 22.574475190679465, 22.565915443935463, 22.558464861408737, 22.62253020231438, 22.62406521281277, 22.62411472899513, 22.60279137694915, 22.61848639903197, 22.76175628479387, 22.764002043458696, 22.761805751241567, 22.762034119165826,22.752653608707142, 22.73203811680016, 22.722858978412297, 22.73227347122288, 22.722858978412297, 22.72653070768359, 22.581855805177874, 22.57617452437228, 22.582772118969004, 22.585104526274105, 22.588674257424803, 22.59569253591314, 22.596911242393666, 22.599964965352953, 22.605063691099968, 22.60972801934469, 22.615036476826322, 22.611618918292017, 22.614882408392226, 22.608943638965496, 22.62236153142111, 22.521717397784897, 22.49547752140118, 22.526650835293196, 22.543243832436914, 22.581131169337798, 22.586846993895623]
longitudes = [88.36844726040026, 88.35531516599767, 88.38685794176858, 88.39578433273505, 88.38093562468507, 88.3906050794681, 88.38667832574968, 88.39241825263318, 88.39646988070382, 88.38993037615415, 88.37009256050914, 88.36980288195615, 88.36665933321436, 88.36471927247482, 88.36976460777771, 88.4795690587448, 88.45762391024049, 88.50233077091443, 88.4798242348902, 88.45992049554907, 88.45648635460978, 88.4656164558199, 88.47285197073856, 88.46404665573748, 88.45778262497343, 88.4377847877931, 88.4333087927997, 88.44165386849609, 88.43368811434455, 88.43390053455822, 88.41229437425525, 88.4192283732789, 88.4255554577272, 88.41220333674616, 88.41382683299777, 88.32329495615791, 88.27025062227008, 88.26260349499313, 88.32899995253605, 88.39830960031705, 88.35970983384125]
# Generate doctor_id starting from 1200
doctor_ids = list(range(1200, 1200 + len(doctor_names)))

# Create a DataFrame
data = {
    'doctor_id': doctor_ids,
    'doctor_name': doctor_names,
    'doctor_rating': doctor_ratings,
    'latitude':latitudes,
    'longitude':longitudes
}

# Convert to a Pandas DataFrame
df = pd.DataFrame(data)

# Display the DataFrame in tabular format
print(df)

df.to_csv('doctors_data.csv', index=False)

print("Data exported to 'doctors_data.csv' successfully!")
