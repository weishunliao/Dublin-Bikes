station_list = ["BLESSINGTON STREET", "BOLTON STREET", "GREEK STREET", "CHARLEMONT PLACE", "CHRISTCHURCH PLACE", "HIGH STREET", "CUSTOM HOUSE QUAY", "EXCHEQUER STREET", "DAME STREET", "EARLSFORT TERRACE", "ECCLES STREET", "FITZWILLIAM SQUARE WEST", "FOWNES STREET UPPER", "HARDWICKE STREET", "GEORGES QUAY", "GOLDEN LANE", "GRANTHAM STREET", "HERBERT PLACE", "LEINSTER STREET SOUTH", "TOWNSEND STREET", "CUSTOM HOUSE", "CATHAL BRUGHA STREET", "MERRION SQUARE EAST", "MERRION SQUARE WEST", "MOLESWORTH STREET", "MOUNTJOY SQUARE WEST", "ORMOND QUAY UPPER", "PARNELL SQUARE NORTH", "PARNELL STREET", "PEARSE STREET", "PRINCES STREET / O'CONNELL STREET", "PORTOBELLO HARBOUR", "SMITHFIELD", "ST. STEPHEN'S GREEN EAST", "ST. STEPHEN'S GREEN SOUTH", "TALBOT STREET", "WILTON TERRACE", "JERVIS STREET", "HARCOURT TERRACE", "SMITHFIELD NORTH", "PORTOBELLO ROAD", "UPPER SHERRARD STREET", "DEVERELL PLACE", "STRAND STREET GREAT", "HERBERT STREET", "EXCISE WALK", "GUILD STREET", "GEORGES LANE", "YORK STREET WEST", "YORK STREET EAST", "NEWMAN HOUSE", "CLONMEL STREET", "HATCH STREET", "MOUNT STREET LOWER", "GRATTAN STREET", "SIR PATRICK DUN'S", "DENMARK STREET GREAT", "NORTH CIRCULAR ROAD", "HARDWICKE PLACE", "LIME STREET", "FENIAN STREET", "SANDWITH STREET", "CONVENTION CENTRE", "NEW CENTRAL BANK", "THE POINT", "HANOVER QUAY", "GRAND CANAL DOCK", "BARROW STREET", "KEVIN STREET", "JOHN STREET WEST", "FRANCIS STREET", "OLIVER BOND STREET", "JAMES STREET", "MARKET STREET SOUTH", "WOLFE TONE STREET", "MATER HOSPITAL", "ECCLES STREET EAST", "ST JAMES HOSPITAL (LUAS)", "ST. JAMES HOSPITAL (CENTRAL)", "MOUNT BROWN", "EMMET ROAD", "BROOKFIELD ROAD", "ROTHE ABBEY", "PARKGATE STREET", "COLLINS BARRACKS MUSEUM", "BLACKHALL PLACE", "FITZWILLIAM SQUARE EAST", "BENSON STREET", "SOUTH DOCK ROAD", "HEUSTON BRIDGE (NORTH)", "HEUSTON STATION (CENTRAL)", "HEUSTON STATION (CAR PARK)", "ROYAL HOSPITAL", "KILMAINHAM LANE", "KILMAINHAM GAOL", "FREDERICK STREET SOUTH", "CITY QUAY", "HEUSTON BRIDGE (SOUTH)", "KING STREET NORTH", "WESTERN WAY", "GRANGEGORMAN LOWER (SOUTH)", "GRANGEGORMAN LOWER (CENTRAL)", "GRANGEGORMAN LOWER (NORTH)", "RATHDOWN ROAD", "CHARLEVILLE ROAD", "AVONDALE ROAD", "BUCKINGHAM STREET LOWER", "PHIBSBOROUGH ROAD", "MOUNTJOY SQUARE EAST", "NORTH CIRCULAR ROAD (O'CONNELL'S)", "MERRION SQUARE SOUTH", "WILTON TERRACE (PARK)", "KILLARNEY STREET"];
autocomplete(document.getElementById("search_box"), station_list);

function autocomplete(inp, arr) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function (e) {
        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) {
            return false;
        }
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        for (i = 0; i < arr.length; i++) {
            /*check if the item starts with the same letters as the text field value:*/
            if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                /*create a DIV element for each matching element:*/
                b = document.createElement("DIV");
                /*make the matching letters bold:*/
                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);
                /*insert a input field that will hold the current array item's value:*/
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                /*execute a function when someone clicks on the item value (DIV element):*/
                b.addEventListener("click", function (e) {
                    /*insert the value for the autocomplete text field:*/
                    inp.value = this.getElementsByTagName("input")[0].value;
                    /*close the list of autocompleted values,
                    (or any other open lists of autocompleted values:*/
                    closeAllLists();
                });
                a.appendChild(b);
            }
        }
    });
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function (e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            /*If the arrow DOWN key is pressed,
            increase the currentFocus variable:*/
            currentFocus++;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 38) { //up
            /*If the arrow UP key is pressed,
            decrease the currentFocus variable:*/
            currentFocus--;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 13) {
            /*If the ENTER key is pressed, prevent the form from being submitted,*/
            e.preventDefault();
            if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (x) x[currentFocus].click();
            }
        }
    });

    function addActive(x) {
        /*a function to classify an item as "active":*/
        if (!x) return false;
        /*start by removing the "active" class on all items:*/
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        /*add class "autocomplete-active":*/
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        /*a function to remove the "active" class from all autocomplete items:*/
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        /*close all autocomplete lists in the document,
        except the one passed as an argument:*/
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }

    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });

}