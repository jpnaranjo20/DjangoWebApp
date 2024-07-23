
// Create the 'selectedSeats' and 'selectedSeats_counter' variables inside of localStorage.
if (!localStorage.getItem('selectedSeats')) {
    localStorage.setItem('selectedSeats', [])
}

if (!localStorage.getItem('selectedSeats_counter')) {
    localStorage.setItem('selectedSeats_counter', 0)
}

// Everytime there's a page reload.
document.addEventListener('DOMContentLoaded', function() {

    // Reset 'selectedSeats' and 'selectedSeats_counter' variables.
    localStorage.setItem('selectedSeats', []);
    localStorage.setItem('selectedSeats_counter', 0);
    
    // If the 'Reserve!' button exists, render it as invisible.
    if (document.querySelector('#res')) {
        document.querySelector('#res').style.display = "none";
    }
    
    // If the part of the page which contains the screen and the seats exists.
    if (document.querySelector('.container')) {
        const container = document.querySelector('.container');

        // Seat select event
        container.addEventListener('click', event => {
            const element = event.target;
            // If the clicked part of the container is a seat and it is not occupied, toggle its class to selected and update the selected seat count.
            if (element.classList.contains('seat') && !element.classList.contains('occupied')) {

                // If a seat has been selected, make the 'Reserve!' button visible. 
                if (document.querySelector('#res')) {
                    document.querySelector('#res').style.display = "block";
                }

                // Toggle class and update seat count.
                element.classList.toggle('selected');
                updateSelectedSeatsCount();

            }
        })
    }

    // If the div that shows the current count exists, set its text to the selectedSeats counter.
    if (document.querySelector('#count')) {
        const count = document.getElementById('count');
        count.innerHTML = localStorage.getItem('selectedSeats_counter');
    }

    // If the div that shows the possible cancellable reservations exists, render it invisible.
    if (document.getElementById('cancel_res_picker')) {
        const picker = document.getElementById('cancel_res_picker');
        picker.style.display = "none";
    }

    // If user is not admin (consumer), make a reservation if he/she clicks on the 'Reserve!' button.
    document.addEventListener('click', event => {
        const element = event.target;
        if (element.getAttribute('id') === "res") {
            id = element.getAttribute('name');
            reserve(id);
        }
    })
    
    // If user is an admin, cancel reservation if 'cancel_res' button is clicked.
    document.addEventListener('click', event => {
        const element = event.target;
        if (element.getAttribute('id') === "cancel_res") {
            id = element.getAttribute('name');
            select_cancel_admin(id);
        }
    })

    // If the user is currently on the view_reservation or make_reservation template, get the film's id from the name attribute of the cancel_res or res buttons. 
    if (window.location.href.includes("make_reservation") || window.location.href.includes("view_reservations")) {
        let username = document.querySelector('strong').innerText;
        if (username.includes("Admin")) {
            id = document.getElementById('cancel_res').name;
        } else {
            id = document.getElementById('res').name;
        }
        // Render the occupied seats according to the obtained film's (via the id) reserved seats.
        preserveOccupied(id);
    }

})

// Function that allows to update the seat count as the user selects or de-selects seats.
const updateSelectedSeatsCount = () => {

    const selectedSeats = document.querySelectorAll('.row_theater .selected');
    const seats = document.querySelectorAll('.row_theater .seat');
    let count = document.getElementById('count');
    
    // The three dot notation serves to apply a function to all the elements inside of the selectedSeats array, in this case, the map function. 
    // seatsIndex is an array of the indeces of each seat. This variable assigns a number to each of the seats in the theater. This number (index) is 
    // used to represent the seats of a Reservation instance in the back-end.
    const seatsIndex = [...selectedSeats].map(seat => [...seats].indexOf(seat));
  
    localStorage.setItem('selectedSeats', JSON.stringify(seatsIndex));
    
    // Variable that represents the current amount of selected seats.
    const selectedSeatsCount = selectedSeats.length;
    localStorage.setItem('selectedSeats_counter', selectedSeatsCount) 

    // Don't show reserve/cancel button unless the user has selected at least one seat.
    if (selectedSeatsCount === 0) {
        if (document.querySelector('#res')) {
            document.querySelector('#res').style.display = "none";
        }
    }
    
    // Show the current count in the corresponding div.
    count.innerHTML = localStorage.getItem('selectedSeats_counter');
};

// Function that allows to make a reservation once the user has selected the desired seats.
function reserve(film_id) {

    // First, get the seat codes for the selected seats.
    var s = localStorage.getItem('selectedSeats');

    // Remove the brackets that are introduced from localStorage
    var seat_numbers = s.substring(1, s.length-1);

    // Create an object from the string by splitting it at the comma. 
    var seat_numbers_obj = seat_numbers.split(',');

    // Create an empty list to fill it with the seat codes (A1,B5,etc...) later on.
    let seat_codes = [];

    // For each seat, get its inner text which is hardcoded to be that specific seat's code, and append it to the seat_codes array.  
    seat_numbers_obj.forEach(seat => {
        let code = document.getElementById(seat).innerText;
        seat_codes.push(code);
    })

    // Convert the array to a string so that it can be saved appropriately to the database later on.
    seat_codes = String(seat_codes);

    // Now, generate a unique n-character reservation ID.
    let n = 5;
    let reservation_id = makeid(n);

    // This function generates a unique length-character ID. It was taken from StackOverflow here: https://stackoverflow.com/questions/1349404/generate-random-string-characters-in-javascript?page=1&tab=votes#tab-top
    // I am not the original author of this function and I do not intend to violate any copyright/plagiarism rules by including this function in my code.
    function makeid(length) {
        var result = '';
        var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        var charactersLength = characters.length;
        for (var i = 0; i < length; i++) {
          result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
       return result;
    }

    // Call the function in the back-end that creates the reservation instance and updates all relevant fields.
    fetch(`/reserve/${film_id}`, {
        method: 'POST',
        body: JSON.stringify({
            "id": film_id,
            "reserved_seats": seat_numbers,
            "seat_codes": seat_codes,
            "reservation_id": reservation_id
        })
    })
    .then(response => response.json())
    .then(result => {

        // Print result
        console.log(result);

        // Get the newly updated film's attributes.
        fetch(`/film/${film_id}`)
        .then(response => response.json())
        .then(film => {

            // For each occupied seat that the film has, render it as occupied and unmark it as selected.
            let occupied = film.reserved_seats;
            let s2 = occupied.split(',');
            console.log(s2);
            s2.forEach(n => f(n))

            function f(n) {
                let seat = document.getElementById(n)
                seat.classList.add('occupied');
                seat.classList.remove('selected');
            }

            // Get the new reserved (occupied) seat amount, and the total amount of seats.
            let reserved_amount = document.querySelectorAll('.seat.occupied').length;
            let total_seat_amount = document.querySelectorAll('.container .seat').length;

            // Update available and reserved seats amount in the database.
            fetch(`/update_seats/${film_id}`, {
                method: "PUT",
                body: JSON.stringify({
                    'reserved_amount': reserved_amount,
                    'available_amount': total_seat_amount - reserved_amount
                })
            })

            // Update the inner HTML in the page.
            document.getElementById('seats_reserved').innerText = reserved_amount;
            document.getElementById('seats_available').innerText = total_seat_amount - reserved_amount;

            // Reset localStorage variables.
            localStorage.setItem('selectedSeats', []);
            localStorage.setItem('selectedSeats_counter', 0);
            document.getElementById('count').innerHTML = localStorage.getItem('selectedSeats_counter');

            // Display alert message informing generated reservation ID.
            let alert = document.createElement('div');
            alert.setAttribute('class', "alert alert-secondary alert-dismissible fade show");
            alert.setAttribute('id', "reservation_id_panel");
            alert.setAttribute('role', "alert");
            alert.setAttribute('style', "margin-top: 10px;")

            let span = document.createElement('span');
            span.setAttribute('id', 'res_message');
            span.innerHTML = `<strong> Reservation confirmed!</strong> Your reservation id is ${reservation_id} </span>`

            let btn = document.createElement('button');
            btn.setAttribute('type', 'button');
            btn.setAttribute('class', 'close');
            btn.setAttribute('data-dismiss', 'alert');
            btn.setAttribute('aria-label', 'Close');

            let span2 = document.createElement('span');
            span2.setAttribute('aria-hidden', 'true');
            span2.setAttribute('id', 'x-btn');
            span2.innerHTML = "&times;";

            // All of these HTML elements were created taking into account that a dismissable message (taken from Bootstrap) follow the following paradigm:
            // <div class="alert alert-secondary alert-dismissible fade show" role="alert" style="display: none;" id="reservation_id_panel">
            //     <span id="res_message"><strong>Reservation confirmed!</strong> Your reservation id is </span>
            //     <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            //     <span aria-hidden="true">&times;</span>
            //     </button>
            // </div>

            // Show the created message.
            btn.append(span2);
            alert.append(span);
            alert.append(btn);
            document.querySelector('#reservation_msg_div').append(alert);

            // Delete the div when the user presses the 'x'.
            alert.querySelector('#x-btn').addEventListener('clcik', event => {
                const element = event.target;
                if (element.getAttribute('id') === "x-btn") {
                    let panel = document.querySelector('#reservation_id_panel');
                    delete panel;
                }
            })
        })
    });
}

// This function allows the admin user to pick a reservation to cancel.
function select_cancel_admin(film_id) {

    // Get the cancel button
    let cancel_btn = document.getElementById('cancel_res');
    cancel_btn.style.display = "none";

    // Display the cancellable reservations div.
    let picker = document.getElementById('cancel_res_picker');
    picker.style.display = "block";
    
    // Call the function in the back-end that gets all reservations for that film.
    fetch(`/get_reservations/${film_id}`)
    .then(response => response.json())
    .then(reservations => {

        console.log(reservations);

        // Create a div for each reservation found for that film and style it according to the website's feel. 
        let reservations_div = document.createElement('div');
        reservations_div.setAttribute('class', 'reservations_div');
        reservations_div.setAttribute('id', 'reservations_div');

        document.querySelector('#cancel_res_picker').append(reservations_div);

        reservations.forEach(res => {
            let res_div = document.createElement('div');
            res_div.setAttribute("class", "res_div");
            
            let res_btn = document.createElement('button');
            res_btn.setAttribute('class', 'reservation_btn');
            res_btn.setAttribute('name', 'res_btn');
            res_btn.setAttribute('id', `${res.id}`);
            res_btn.setAttribute('style', 'display: inline-block; margin-top: 10px;');
            res_btn.innerText = `User: ${res.reserver}, seats ${res.seats_code}`;

            res_div.append(res_btn);
            reservations_div.append(res_div);

            // Cancel the reservation associated with each button.
            res_btn.addEventListener('click', event => {
                const element = event.target;

                // Get the id of the reservation we wish to cancel. 
                if (element.getAttribute('name') === 'res_btn') {
                    id = element.getAttribute('id');

                    // Call the function that cancels the reservation in the back-end and updates other relevant variables, like available and reserved seats.
                    fetch(`/cancel_reservation/${id}`, {
                        method: 'POST',
                        body: JSON.stringify({
                            "seats_number": res.seats_number
                        })
                    })
                    .then(response => response.json())
                    .then(result => {
                        // This fetch call returns a JSON object that represents the number of reserved and available seats after having deleted the corresponding seats.
                        console.log(result);
                        document.getElementById('seats_reserved').innerText = result.reserved_seats_amount_new;
                        document.getElementById('seats_available').innerText = result.seats_available_new;
                        
                        // Render the previously occupied seats as available.
                        let obj = result.seats_number_res.split(',');
                        obj.forEach(number => {
                            let seat = document.getElementById(number);
                            seat.classList.toggle('occupied');
                        })
                    })

                    // Hide each reservation div that was previously created as the user clicks on it.
                    document.getElementById(id).parentElement.style.display = "none";

                    // These lines assert that the cancel_res_picker div disappears if the admin is done cancelling all reservations. 
                    let counter = 0;
                    let ress = document.querySelectorAll('.res_div');
                    ress.forEach(res => {
                        if (res.style.display === "none") {
                            counter++;
                            if (counter === document.querySelector('#reservations_div').childElementCount) {
                                document.querySelector('#cancel_res_picker').style.display = "none";
                                counter = 0;
                            }
                        }
                    })
                }
            })
        });
    });
}

// This function asserts that all occupied seats for a specific film are rendered as occupied on every page reload. 
function preserveOccupied(film_id) {

    // Get the film's attributes
    fetch(`/film/${film_id}`)
    .then(response => response.json())
    .then(film => {
        console.log(film);

        // Focus on the film's string of reserved_seats
        let str = film.reserved_seats;

        // If there are reserved seats for that film
        if (str !== "") {
            console.log(str);

            let str2 = str.split(',');
            str2.forEach(n => f(n))
            
            // Add class occupied (render as occupied) to each seat whose number is in the reserved_seats attribute of the film.
            function f(n) {
                let seat = document.getElementById(n);
                seat.classList.add('occupied');
            }
        }
    })
}