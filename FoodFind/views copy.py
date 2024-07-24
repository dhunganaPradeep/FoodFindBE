from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.http import HttpResponseRedirect
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User

# def admin_login(request):

#     try:
#         if request.user.is_authenticated:
#             return redirect('/dashboard/')

#         if request.method == 'POST':
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user_obj = User.objects.filter(
#                 username=username).first()  # Get the first user object

#             if not user_obj:
#                 messages.error(request, 'Account not found')
#                 return redirect('admin_login')

#             user = authenticate(request, username=username, password=password)

#             if user and user.is_superuser:
#                 login(request, user)
#                 return redirect('/dashboard/')
#             else:
#                 messages.error(request, 'Invalid username or password')
#                 return redirect('admin_login')

#         return render(request, 'login.html')

#     except Exception as e:
#         print(e)
