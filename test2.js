app.get('/vulnerable', (req, res) => {
 if (req.query.url) {
 	res.redirect(req.query.url);
 } else {
 	res.redirect('<https://www.example.com>');
 }
});
