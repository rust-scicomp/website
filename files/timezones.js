let cookie_settings = "expires=Mon, 01 Jan 2024 12:00:00 UTC; path=/; SameSite=Lax";

let zone = "BST"

let tzdata = {
    "BST": [1, 0, "BST [UTC+1]"],

    "PDT": [-7, 0, "Pacific Time [UTC-7]"],
    "MDT": [-6, 0, "Mountain Time [UTC-6]"],
    "CDT": [-5, 0, "Central Time [UTC-5]"],
    "EDT": [-5, 0, "Eastern Time [UTC-4]"],
    "GMT": [0, 0, "GMT [UTC&plusmn;0]"],
    "WEST": [1, 0, "WEST [UTC+1]"],
    "CEST": [2, 0, "CEST [UTC+2]"],
    "EEST": [3, 0, "EEST [UTC+3]"],

    "UTC-12": [-12, 0, "UTC-12"],
    "UTC-11": [-11, 0, "UTC-11"],
    "UTC-10": [-10, 0, "UTC-10 (Honolulu)"],
    "UTC-9:30": [-9, 30, "UTC-9:30"],
    "UTC-9": [-9, 0, "UTC-9"],
    "UTC-8": [-8, 0, "UTC-8 (Anchorage)"],
    "UTC-7": [-7, 0, "UTC-7 (Los Angeles, San Diego, Vancouver, Tijuana)"],
    "UTC-6": [-6, 0, "UTC-6 (Denver, Edmonton, Cuidad Ju&aacute;rez, Guatemala City)"],
    "UTC-5": [-5, 0, "UTC-5 (Houston, Winnipeg, Lima, Kingston)"],
    "UTC-4": [-4, 0, "UTC-4 (Havana, New York, Washington D.C., Toronto, London, Caracas)"],
    "UTC-3:30": [-3, 30, "UTC-3:30"],
    "UTC-3": [-3, 0, "UTC-3 (Santiago, Sao P&atilde;ulo, Rio de Janeiro, Montevideo, Buenos Aires)"],
    "UTC-2": [-2, 0, "UTC-2"],
    "UTC-1": [-1, 0, "UTC-1"],
    "UTC": [0, 0, "UTC (Dakar)"],
    "UTC+1": [1, 0, "UTC+1 (London, Lisbon, Lagos, Algiers, Dublin, King's Lynn)"],
    "UTC+2": [2, 0, "UTC+2 (Madrid, Vatican, Paris, Rome, Vienna, Warsaw, Germany, Cairo, Johannesburg)"],
    "UTC+3": [3, 0, "UTC+3 (Kyiv, Athens, Sofia, Addis Ababa, Istanbul, Moscow, Riyadh)"],
    "UTC+3:30": [3, 30, "UTC+3:30 (Tehran)"],
    "UTC+4": [4, 0, "UTC+4 (Dubai, Baku)"],
    "UTC+4:30": [4, 30, "UTC+4:30 (Kabul)"],
    "UTC+5": [5, 0, "UTC+5 (Karachi)"],
    "UTC+5:30": [5, 30, "UTC:5:30 (Mumbai, Columbo)"],
    "UTC+5:45": [5, 45, "UTC+5:45 (Kathmandu))"],
    "UTC+6": [6, 0, "UTC+6 (Almaty, Dhaka)"],
    "UTC+6:30": [6, 30, "UTC+6:30 (Yangon)"],
    "UTC+7": [7, 0, "UTC+7 (Bangkok, Jakarta)"],
    "UTC+8": [8, 0, "UTC+8 (Perth, Bander Seri Begawan, Beijing, Singapore, Kuala Lumpur, Taipei, Shanghai)"],
    "UTC+8:45": [8, 45, "UTC+8:45"],
    "UTC+9": [9, 0, "UTC+9 (Soeul, Tokyo, Pyongyang)"],
    "UTC+9:30": [9, 30, "UTC+9:30 (Adelaide)"],
    "UTC+10": [10, 0, "UTC+10 (Sydney, Vladivostok, Port Moresby)"],
    "UTC+10:30": [10, 30, "UTC+10:30"],
    "UTC+11": [11, 0, "UTC+11"],
    "UTC+12": [12, 0, "UTC+12 (Suva)"],
    "UTC+12:45": [12, 45, "UTC+12:45"],
    "UTC+13": [13, 0, "UTC+13 (Wellington, Auckland)"],
    "UTC+14": [14, 0, "UTC+14"],
    "Unix time": [0, 0, "Unix time"],
}
let months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
let days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

decoded_cookie = decodeURIComponent(document.cookie)
ca = decoded_cookie.split(";")
for (let i = 0; i < ca.length; i++) {
    let c = ca[i]
    while (c.charAt(0) == " "){c = c.substring(1);}
    if (c.indexOf("tz=") == 0){
        zone = c.substring(3);
    }
}

function change_timezone_dropdown(tz){
    if (document.getElementById("tzone")) {
        document.getElementById("tzone").innerHTML = tz
    }
    zone = tz
    document.cookie = "tz=" + tz + "; " + cookie_settings
    update_timezones()
    if (document.getElementById("tzonechange")) {
        document.getElementById("tzonechange").style.display = "none"
    }
}

ee = document.getElementsByClassName("bst-time")[0]

function zeropad(n, digits)
{
    let out = "" + n;
    while(out.length < digits){ out = "0" + n; }
    return out;
}

function update_timezones(){
    es = document.getElementsByClassName("bst-time")
    for (let i = 0; i < es.length; i++){
        if (zone == "Unix time")
        {
            let date = new Date(Date.UTC(2023, 7, 13, es[i].dataset["hour"], es[i].dataset["minute"], 0, 0))
            date = new Date(date.getTime() - 1 * 60 * 60 * 1000 + tzdata[zone][1] * 60 * 1000);
            es[i].innerHTML = date.getTime() / 1000;

        } else {

            let date = new Date(Date.UTC(2023, 7, 13, es[i].dataset["hour"], es[i].dataset["minute"], 0, 0))

            date = new Date(date.getTime() + (tzdata[zone][0] - 1) * 60 * 60 * 1000 + tzdata[zone][1] * 60 * 1000);

            let h12 = date.getUTCHours()
            let ampm = "AM"
            if (h12 >= 12) {h12 -= 12; ampm = "PM";}
            if (h12 == 0) {h12 = 12}

            time = es[i].dataset["format"]

            dth = date.getUTCDate()
            if (dth == 1 || dth == 21 || dth == 31) {dth += "st"}
            else if (dth == 2 ||  dth == 22) {dth += "nd"}
            else {dth += "th"}

            time = time.replace(/\{YEAR\}/g, date.getUTCFullYear());
            time = time.replace(/\{MONTH\}/g, date.getUTCMonth());
            time = time.replace(/\{MONTHNAME\}/g, months[date.getUTCMonth()]);
            time = time.replace(/\{DATE\}/g, date.getUTCDate());
            time = time.replace(/\{DATETH\}/g, dth);
            time = time.replace(/\{WEEKDAY\}/g, days[date.getUTCDay()]);
            time = time.replace(/\{AM\/PM\}/g, ampm);
            time = time.replace(/\{am\/pm\}/g, ampm.toLowerCase());
            time = time.replace(/\{HOUR\}/g, date.getUTCHours());
            time = time.replace(/\{0HOUR\}/g, zeropad(date.getUTCHours(), 2));
            time = time.replace(/\{24 HOUR\}/g, date.getUTCHours());
            time = time.replace(/\{24 0HOUR\}/g, zeropad(date.getUTCHours(), 2));
            time = time.replace(/\{12 HOUR\}/g, h12);
            time = time.replace(/\{12 0HOUR\}/g, zeropad(h12, 2));
            time = time.replace(/\{MINUTE\}/g, zeropad(date.getUTCMinutes(), 2));
            if (date.getUTCMinutes() == 0)
            {
                time = time.replace(/\{\?:MINUTE\}/g, "");
            } else {
                time = time.replace(/\{\?:MINUTE\}/g, ":" + zeropad(date.getUTCMinutes(), 2));
            }
            time = time.replace(/\{TZ\}/g, zone);

            es[i].innerHTML = time;
        }
    }
}

function page_load_update_timezone(){
    e = document.getElementById("tzselect")
    keys = Object.keys(tzdata)
    for (let i = 0; i < keys.length; i++){
        let opt = document.createElement('option');
        opt.value = keys[i];
        opt.innerHTML = tzdata[keys[i]][2];
        e.appendChild(opt);

        if (keys[i] == zone){
            e.selectedIndex = i;
            if (document.getElementById("tzone")) {
                document.getElementById("tzone").innerHTML = zone
            }
        }
    }
    update_timezones()
}

function show_tz_change(){
    document.getElementById("tzonechange").style.display = "block"
}
