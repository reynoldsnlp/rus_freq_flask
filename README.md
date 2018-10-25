# rus_freq_flask
Sort user's list of Russian words by frequency (using Sharoff's lemma frequency list)

#Here is a high level overview of the code and style. 
The web interface is pretty simple. There is the main landing page at freq_form.html and a results page at freq_output.html. The banner image for both pages is in the images folder and can be changed to any image renamed to banner.jpg. When more languages are added, I would recommend building it into a single page app. There is no real reason why it needs to redirect to a different page. If this is not worth building because of time, more routes will need to be added to the backend and I would recommend making a navigation component. There is already navigation hrefs in the main page that are commented out. -kp