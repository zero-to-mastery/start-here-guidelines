//https://zenquotes.io/   ı have to make like tis website


const quoteContainer = document.getElementById('quote-container');
const quoteText = document.getElementById('quote');
const authorText = document.getElementById('author');
const twitterBtn = document.getElementById('twitter');
const newQuoteBtn = document.getElementById('new-quote');
const loader = document.getElementById('loader');

let apiQuotes = [];
//Show Loading
function loading(){
  quoteContainer.hidden = true;
  loader.hidden = false;
}
//Hide Loading
function complete(){
  quoteContainer.hidden = false;
  loader.hidden = true;
}

//Show New Quote
 function newQuote(){
  loading();
    //Pick a random quote from  apiQuotes array 
   const quote = apiQuotes[Math.floor(Math.random() * apiQuotes.length)];
    //const quote = apiQuotes[Math.floor(Math.random() * apiQuotes.length)];
    //Check if author field is blank and replace it with Unknown.
    if(!quote.author){
        authorText.textContent = 'Unknown';
    }
else{
    authorText.textContent = quote.author;
    }
    //Check  Quote length to determine styling.
    if(quote.text.length > 120){
      quoteText.classList.add('long-quote');
    }
    else{
      quoteText.classList.remove('long-quote');
        }
        //Set Quote , Hide loader
        
    quoteText.textContent = quote.text;
    complete();
}
//Get Quotes from ApI
async function getQuotes() {
 loading();
  const apiUrl = 'https://jacintodesign.github.io/quotes-api/data/quotes.json';
  try {
    const response = await fetch(apiUrl);
    apiQuotes = await response.json();
   // console.log(apiQuotes);
    newQuote();
  } catch (error) {
    // Catch Error Here
  }
}
//Tweet Quote
function TweetQuote(){
    const tweetUrl = `https://twitte.com/intent/tweet?${text-Content.innerText} - ${authorText.textContent.innerText}`;
    window.open((tweetUrl, '_blank'));
}

//Event Listners
newQuoteBtn.addEventListener('click', newQuote);
twitterBtn.addEventListener('click', TweetQuote)

//On Load
getQuotes();
 


