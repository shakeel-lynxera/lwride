

#-------------------------------------------------------------
#-------------------------------------------------------------
#-------------------------------------------------------------
#-------------------------------------------------------------
#-------------------------------------------------------------
#-------------------------------------------------------------
#-------------------------------------------------------------
#-------------------------------------------------------------
#-------------------------------------------------------------
#-------------------------------------------------------------






from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
import pyrebase
import datetime
from EAdda.settings import config

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()


#Admin home/dashboard page
def adminHome(request):
	if request.session.has_key('userId'):
		countAdmins=countCaptains=countPassengers=countBlockedCaptains=countBlockedPassengers=countnotifications=countAllRides=countCurrentRides=0
		
		adminData = database.child('users').child('admin').get().val()
		for i in adminData:
			countAdmins=countAdmins+1

		captainData = database.child('users').child('captain').get().val()
		for i in captainData:
			countCaptains=countCaptains+1
			if captainData[i]['status'] == '0':
				countBlockedCaptains=countBlockedCaptains+1

		passengersData = database.child('users').child('passenger').get().val()
		for i in passengersData:
			countPassengers=countPassengers+1
			if passengersData[i]['status'] == '0':
				countBlockedPassengers=countBlockedPassengers+1

		passengersData = database.child('users').child('passenger').get().val()
		fetchData=[]
		for i in passengersData:
			passengersData[i]['id'] = i
			fetchData.append(passengersData[i])


		currentRides = database.child('rides').child('current_rides').child("captain_rides").get().val()
		for i in currentRides:
			countCurrentRides=countCurrentRides+1


		allRides = database.child('rides').child('all_rides').child("captains_rides").get().val()
		for i in allRides:
			for j in allRides[i]:
				countAllRides=countAllRides+1

		notifications = database.child('notifications').child('admins').get().val()
		for i in notifications:
			countnotifications=countnotifications+1

		return render(request, 'admin_home.html', {'countAdmins' : countAdmins, 'countCaptains':countCaptains, 'countPassengers':countPassengers,
			'countBlockedPassengers':countBlockedPassengers, 'countBlockedCaptains':countBlockedCaptains, 'countCurrentRides':countCurrentRides,
			'countAllRides':countAllRides,'countnotifications':countnotifications })
	else:
		return redirect('admin_login')

#First login Page
def adminLogin(request):
	if request.session.has_key('userId'):
		return redirect('admin_home')
	return render(request, 'admin_login.html')
	
#Check the login form data for authentication
def checkForLogin(request):

	email = request.POST.get('email')
	password = request.POST.get('password')
	if (email is None) or (str(email).strip()==""):	
		messege = "Fields are empty"
		return render(request, 'admin_login.html', {"messege":messege})
	else:
		try:
			user = auth.sign_in_with_email_and_password(email, password)
			userId = user['localId']
			name = database.child('users').child('admin').child(userId).child('name').get().val()
		except:
			messege = "Invalid email/password"
			return render(request, 'admin_login.html', {"messege":messege})
		request.session['name'] = name
		request.session['userId'] = userId
		return redirect('admin_home')

#Add Captain and vehicle page
def addCaptain(request):
	if request.session.has_key('userId'):
		captainData = database.child('users').child('captain').get().val()
		fetchData=[]
		for i in captainData:
			captainData[i]['id'] = i
			fetchData.append(captainData[i])
		return render(request, 'add_captain.html', {"captainData":fetchData})
	else:
		return redirect('admin_login')

def addAdmin(request):
	if request.session.has_key('userId'):
		return render(request, 'add_admin.html')
	else:
		return redirect('admin_login')

def removeAdmin(request):
	if request.session.has_key('userId'):
		adminId = request.POST.get('id')
		database.child("users").child("admin").child(adminId).child('status').set("")
		database.child("users").child("admin").child(adminId).child('name').set("")
		database.child("users").child("admin").child(adminId).child('email').set("")
		database.child("users").child("admin").child(adminId).child('password').set("")
		return redirect('admin_records')
	else:
		return redirect('admin_login')


#Upload captain and vehicle data from add_captain.html page
def uploadCaptainAndVehicleRecord(request):
	captain_id = request.POST.get('captain_id')
	captainName = request.POST.get('name')
	gender = request.POST.get('gender')
	address = request.POST.get('address')
	cnic = request.POST.get('cnic')
	phoneNumber = request.POST.get('number')
	driverImageUrl = request.POST.get('driver_image_url')
	model = request.POST.get('model')
	numberPlate = request.POST.get('number_plate')
	seats = request.POST.get('seats')
	vehicleType = request.POST.get('vehicle_type')
	vehicleImageUrl = request.POST.get('vehicle_image_url')

	captainData = {

		'captain_name' : captainName,
		'gender' : gender,
		'rating' : "5",
		'address' : address,
		'cnic' : cnic,
		'phone_number' : phoneNumber,
		'status' : "1",
		'driver_image_url' : driverImageUrl,
		'model' : model,
		'number_plate' : numberPlate,
		'seats' : seats,
		'vehicle_type' : vehicleType,
		'vehicle_image_url' : vehicleImageUrl
	}
	database.child("users").child("captain").child(captain_id).set(captainData)
	return redirect('captains_records')


#update captian records
def captainUpdateRecords(request):
	captain_id = request.POST.get('captain_id')
	fetchData = database.child('users').child('captain').child(captain_id).get().val()
	captainData=[]
	for i in fetchData:
		captainData = fetchData
	return render(request, 'captain_update_records.html', {"captainData":captainData, "captain_id":captain_id})

#upload update captain records
def updateCaptainAndVehicleRecord(request):
	captain_id = request.POST.get('captain_id')
	captainName = request.POST.get('name')
	gender = request.POST.get('gender')
	address = request.POST.get('address')
	cnic = request.POST.get('cnic')
	phoneNumber = request.POST.get('number')
	driverImageUrl = request.POST.get('driver_image_url')
	model = request.POST.get('model')
	numberPlate = request.POST.get('number_plate')
	seats = request.POST.get('seats')
	vehicleType = request.POST.get('vehicle_type')
	vehicleImageUrl = request.POST.get('vehicle_image_url')

	captainData = {

		'captain_name' : captainName,
		'gender' : gender,
		'rating' : "5",
		'address' : address,
		'cnic' : cnic,
		'phone_number' : phoneNumber,
		'status' : "1",
		'driver_image_url' : driverImageUrl,
		'model' : model,
		'number_plate' : numberPlate,
		'seats' : seats,
		'vehicle_type' : vehicleType,
		'vehicle_image_url' : vehicleImageUrl
	}
	database.child("users").child("captain").child(captain_id).set(captainData)
	return redirect('captains_records')



def uploadAdminRecord(request):
	name = request.POST.get("name")
	email = request.POST.get("email")
	password = request.POST.get("password")
	try:
		user = auth.create_user_with_email_and_password(email, password)
	except:
		return render(request, 'add_admin.html')
	userId = user['localId']
	data = {"name":name, "email":email, "password":password, "status":"1"}
	database.child("users").child("admin").child(userId).set(data)
	return redirect('admin_records')

#Show all the current Admins
def adminRecords(request):
	if request.session.has_key('userId'):
		adminData = database.child('users').child('admin').get().val()
		fetchData=[]
		for i in adminData:
			adminData[i]['id'] = i
			fetchData.append(adminData[i])
		return render(request, 'admin_records.html', {"fetchData":fetchData})
	else:
		return redirect('admin_login')

#Show all the current captain
def captainsRecords(request):
	if request.session.has_key('userId'):
		captainData = database.child('users').child('captain').get().val()
		fetchData=[]
		for i in captainData:
			captainData[i]['id'] = i
			fetchData.append(captainData[i])
		return render(request, 'captains_records.html', {"fetchData":fetchData})
	else:
		return redirect('admin_login')

#Show all passengers 
def passengersRecords(request):
	if request.session.has_key('userId'):
		passengersData = database.child('users').child('passenger').get().val()
		fetchData=[]
		for i in passengersData:
			passengersData[i]['id'] = i
			fetchData.append(passengersData[i])
		return render(request, 'passengers_records.html', {"fetchData":fetchData})
	else:
		return redirect('admin_login')


#Show Captain's all rides
def captainAllRides(request):
	if request.session.has_key('userId'):
		captId = request.POST.get('captain_id')
		allRides = database.child('rides').child('all_rides').child("captains_rides").child(captId).get().val()
		fetchData=[]

		if allRides == None:
			return render(request, 'captain_all_rides.html', {"fetchData":fetchData})

		for i in allRides:
			fetchData.append(allRides[i])
		return render(request, 'captain_all_rides.html', {"fetchData":fetchData})
	else:
		return redirect('admin_login')

#Show Passenger's all rides
def passengersAllRides(request):
	if request.session.has_key('userId'):
		passengerId = request.POST.get('passenger_id')
		allRides = database.child('rides').child('all_rides').child("passenger_rides").child(passengerId).get().val()
		fetchData=[]
		if allRides == None:
			return render(request, 'passenger_all_rides.html', {"fetchData":fetchData})
		for i in allRides:
			fetchData.append(allRides[i])
		return render(request, 'passenger_all_rides.html', {"fetchData":fetchData})
	else:
		return redirect('admin_login')

#Show all currents ride
def currentRide(request):
	if request.session.has_key('userId'):
		currentRides = database.child('rides').child('current_rides').child("captain_rides").get().val()
		fetchData=[]
		for i in currentRides:
			currentRides[i]['id'] = i
			fetchData.append(currentRides[i])
		return render(request, 'current_ride.html', {"fetchData":fetchData})
	else:
		return redirect('admin_login')

#Show all blocked captain
def blockedCaptains(request):
	if request.session.has_key('userId'):
		captainData = database.child('users').child('captain').get().val()
		fetchData=[]
		for i in captainData:
			captainData[i]['id'] = i
			fetchData.append(captainData[i])
		return render(request, 'blocked_captains.html', {"fetchData":fetchData})
	else:
		return redirect('admin_login')

def addToBlockCaptain(request):
	if request.session.has_key('userId'):
		captId = request.POST.get('id')
		reason = request.POST.get('reason')
		database.child("users").child("captain").child(captId).child('status').set("0")
		database.child("users").child("captain").child(captId).child('reason').set(reason)
		return redirect('blocked_captains')
	else:
		return redirect('admin_login')

def removeBlockCaptain(request, id):
	if request.session.has_key('userId'):
		database.child("users").child("captain").child(id).child('status').set("1")
		database.child("users").child("captain").child(id).child('reason').set("")
		return redirect("captains_records")
	else:
		return redirect('admin_login')
	

#Show all blocked passengers
def blockedPassengers(request):
	if request.session.has_key('userId'):
		passengersData = database.child('users').child('passenger').get().val()
		fetchData=[]
		for i in passengersData:
			passengersData[i]['id'] = i
			fetchData.append(passengersData[i])
		return render(request, 'blocked_passengers.html', {"fetchData":fetchData})
	else:
		return redirect('admin_login')

def addToBlockPassenger(request):
	if request.session.has_key('userId'):
		passengerId = request.POST.get('id')
		reason = request.POST.get('reason')
		database.child("users").child("passenger").child(passengerId).child('status').set("0")
		database.child("users").child("passenger").child(passengerId).child('reason').set(reason)
		return redirect('blocked_passengers')
	else:
		return redirect('admin_login')


def removeBlockPassenger(request, id):
	if request.session.has_key('userId'):
		database.child("users").child("passenger").child(id).child('status').set("1")
		database.child("users").child("passenger").child(id).child('reason').set("")
		return redirect('passengers_records')
	else:
		return redirect('admin_login')

#Show all notifications to admin
def notifications(request):
	if request.session.has_key('userId'):

		countCaptainNotifications = countPassengerNotifications = countAdminNotifications = 0

		adminNotifications = database.child('notifications').child('admins').get().val()
		for i in adminNotifications:
			countAdminNotifications=countAdminNotifications+1

		captainNotifications = database.child('notifications').child('captains').get().val()
		for i in captainNotifications:
			countCaptainNotifications=countCaptainNotifications+1

		passengerNotifications = database.child('notifications').child('passengers').get().val()
		for i in passengerNotifications:
			countPassengerNotifications=countPassengerNotifications+1


		return render(request, 'notifications.html', {'countAdminNotifications' : countAdminNotifications,
		 'countCaptainNotifications' : countCaptainNotifications, 'countPassengerNotifications' : countPassengerNotifications})
	else:
		return redirect('admin_login')

#Notify all Captains
def notifyAllCaptains(request):
	if request.session.has_key('userId'):
		messege = request.POST.get('messege')
		date = str(datetime.datetime.today()).split()[0]
		notificationData = {
			'messege' : messege,
			'date' : date
		}
		database.child("notifications").child("captains").push(notificationData)
		return redirect('notifications')
	else:
		return redirect('admin_login')	


#Notify all Passengers
def notifyAllPassengers(request):
	if request.session.has_key('userId'):
		messege = request.POST.get('messege')
		date = str(datetime.datetime.today()).split()[0]
		notificationData = {
			'messege' : messege,
			'date' : date
		}
		database.child("notifications").child("passengers").push(notificationData)
		return redirect('notifications')
	else:
		return redirect('admin_login')	

#Notify all Admins
def notifyAllAdmins(request):
	if request.session.has_key('userId'):
		messege = request.POST.get('messege')
		date = str(datetime.datetime.today()).split()[0]
		notificationData = {
			'messege' : messege,
			'date' : date
		}
		database.child("notifications").child("admins").push(notificationData)
		return redirect('notifications')
	else:
		return redirect('admin_login')

#user logout and redirect to login page
def logout(request):
	del request.session['userId']
	del request.session['name']
	return redirect('admin_login')

