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
		count_available_driver = 0
		count_drivers = 0
		count_ride_requests = 0
		count_users = 0

		try:
			available_driver_data = database.child('availableDrivers').get().val()
			for i in available_driver_data:
				count_available_driver+=1

			driver_data = database.child('drivers').get().val()
			for i in driver_data:
				count_drivers+=1

			ride_request_data = database.child('rideRequest').get().val()
			for i in ride_request_data:
				count_ride_requests+=1
			
			user_data = database.child('users').get().val()
			for i in user_data:
				count_users+=1
		except:
			pass

		return render(request, 'admin_home.html',
			{ 
			'count_available_driver':count_available_driver, 
			'count_drivers':count_drivers,
			'count_ride_requests':count_ride_requests, 
			'count_users':count_users
			}
		)
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
			request.session['name'] = "Sami Ullah"
			request.session['userId'] = "thisIdShouldBeUniqueFromOtherUser"
		except:
			messege = "Invalid email/password"
			return render(request, 'admin_login.html', {"messege":messege})
		return redirect('admin_home')

def drivers(request):
    data_list_=[]
    try:
	    drivers_ = database.child('drivers').get().val()
	    for i in drivers_:
		    drivers_[i]['id'] = i
		    data_list_.append(drivers_[i])
    except:
    	pass
    return render(request, 'driver_list.html',{"drivers_data":data_list_})


def available_drivers(request):
    data_list_=[]
    try:
	    drivers_ = database.child('availableDrivers').get().val()
	    for i in drivers_:
	    	drivers_[i]['id'] = i
	    	data_list_.append(drivers_[i])
    except:
	    pass
    return render(request, 'available_drivers.html',{"drivers_data":data_list_})

def ride_request(request):
    data_list_=[]
    try:
	    rides_ = database.child('rideRequest').get().val()
	    for i in rides_:
	    	rides_[i]['id'] = i
	    	data_list_.append(rides_[i])
    except:
    	pass
    return render(request, 'ride_request.html',{"ride_data":data_list_})

def delete_object(request, id):
    print(id)
    # try:
	#     database.child("drivers").child(id).set("")
    # except:
	#     database.child('rideRequest').child(id).set("")
    return redirect(request.META['HTTP_REFERER'])



#user logout and redirect to login page
def logout(request):
	del request.session['userId']
	del request.session['name']
	return redirect('admin_login')