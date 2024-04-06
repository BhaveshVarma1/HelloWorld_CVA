console.log("Hello world")

window.SpeechRecognitionAlternative = window.SpeechRecognitionAlternative || window.webkitSpeechRecognition

const recognition = new SpeechRecognitionAlternative();
recognition.interimResults = true;

let p = document.createElement('p');
const words = document.querySelector('.words'); words.appendChild(p);


url = window.location.href + "/process"

function postJSON(url, jsonString) {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json; charset=utf-8");

    xhr.onload = function () {
        if (this.status >= 200 && this.status < 300) {
            console.log("Success! Response:", this.responseText);
            recognition.start()
        } else {
            console.error("Error! Response:", this.responseText);
        }
    };

    xhr.onerror = function () {
        console.error("Network error occurred.");
    };

    xhr.send(jsonString);
}

var url = window.location.href + "process"


recognition.addEventListener('end', e => {

})

recognition.addEventListener('result', e => {
    // console.log(e)
    const transcripts = Array.from(e.results)
        .map(result => result[0])
        .map(result => result.transcript)
        .join('')

    console.log(transcripts)

    if (e.results[0].isFinal) {
        const myString = transcripts;
        const myJSON = JSON.stringify({ data: myString });
        postJSON(url,myJSON)
    }
});

recognition.start();

console.log("Hello")