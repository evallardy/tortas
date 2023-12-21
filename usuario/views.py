from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.

@login_required
def cambia_contrasena(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # importante para mantener la sesión del usuario activa
            return redirect('elabora')  # cambia esto por la url a la que quieres redirigir al usuario después de actualizar la contraseña
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/cambia_contrasena.html', {'form': form})