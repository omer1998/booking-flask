
const specialization = document.getElementById('specialization');

const otherSpecialization = document.getElementById('other-specialization');
specialization.addEventListener('change', (e) => {
   
    if (e.target.value === 'other') {
        otherSpecialization.classList.remove('hidden');
        // alert(e.target.classList)
    } else {
        otherSpecialization.classList.add('hidden');
    }
});

document.getElementById("map-location-btn").addEventListener('click', getDoctorLocation);

function getDoctorLocation() {
    navigator.geolocation.getCurrentPosition((position) => {
        const location = {
            long: position.coords.longitude,
            lat: position.coords.latitude
        }
        document.getElementById('longitude').value = location.long;
        document.getElementById('latitude').value = location.lat;
        alert(`Your clinic location is ${location.lat + " " + location.long}`)
}, 
    (error) => {
        alert(error.message)
    });
}