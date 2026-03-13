let bp_b = document.getElementById("bp_r_b");
let bp_t = document.getElementById("bp_r_v");

// Ecoute lorsque la sourie passe sur le front ou back du BP pour activer la fonction css d'extention.
// Ecoute également le moment du départ pour arreter la fonction.


bp_b.addEventListener("mouseenter",function (event) {bp_t.classList.add('extantion_du_territoire');});
bp_b.addEventListener("mouseleave",function (event) {bp_t.classList.remove('extantion_du_territoire');});

bp_t.addEventListener("mouseenter",function (event) {bp_t.classList.add('extantion_du_territoire');});
bp_t.addEventListener("mouseleave",function (event) {bp_t.classList.remove('extantion_du_territoire');});