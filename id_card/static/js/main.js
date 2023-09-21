function defaultImage() {
    var img = document.getElementById('sidebar-profile')
    img.setAttribute('src', "{{ url_for('static', filename='img/profile.jpg') }}")
}