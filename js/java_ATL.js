// Récupération des éléments du DOM
const nextBtn = document.getElementById('nextBtn');
const prevBtn = document.getElementById('prevBtn');

const creation_scan = document.getElementById('arrow_creation_scan');
const reveil_LDD = document.getElementById('arrow_reveil_LDD');
const remonte_scan = document.getElementById('arrow_remonte_scan');
const analyse_scan = document.getElementById('arrow_analyse_scan');

const animation_scan = document.getElementById('animation_scan');
const image_parametre = document.getElementById('image_parametre');

const resArrow = document.getElementById('resArrow');
const stepDesc = document.getElementById('stepDesc');


// Configuration de la machine à états
let currentStep = 0;
const maxSteps = 6;

// Textes explicatifs pour chaque étape
const descriptions = [
    "Étape 0 : L'ATL attend le delay fixé pour déclencher sa requête.",
    "Étape 1 : L'ATL fait un enchainement de requête pour créer la demande d'activation du produit sur la plateforme.",
    "Étape 2 : Le serveur réveil le produit avec sa commande à éxécuter.",
    "Étape 3 : Le produit traite la demande.",
    "Étape 4 : Les résultats sont remontés au serveur.",
    "Étape 5 : L'ARL vient après un délai d'attente, récupérer les résultats de la commande.",
    "Étape 6 : L'ARL peut ensuite traiter les données récoltés et les stocker."
];

function updateAnimation() {
    // 1. Mise à jour de l'état des boutons (grisés ou actifs)
    prevBtn.disabled = currentStep === 0;
    nextBtn.disabled = currentStep === maxSteps;

    // 2. Mise à jour du texte
    stepDesc.textContent = descriptions[currentStep];
	
	// -- ANIMATION DES FLECHES -- //
    // 3. Étape 1 => Création Scan  
    if (currentStep == 1) {
        creation_scan.classList.add('active');
    } else {
        creation_scan.classList.remove('active');
    }
    // 4. Étape 2 => Réveil du LDD 
    if (currentStep == 2) {
        reveil_LDD.classList.add('active');
    } else {
        reveil_LDD.classList.remove('active');
    }
	// 5. Étape 3 => Scan radar 
    if (currentStep == 3) {
		animation_scan.classList.add('active');
    } else {
        animation_scan.classList.remove('active');
	}
	// 6. Étape 4 => Remontée du scan  
    if (currentStep == 4) {
		remonte_scan.classList.add('active');
    } else {
        remonte_scan.classList.remove('active');
	}
	// 7. Étape 5 => Récupère le scan   
    if (currentStep == 5) {
		analyse_scan.classList.add('active');
    } else {
        analyse_scan.classList.remove('active');
	}
	// 8. Étape 6 => Analyse du scan   
    if (currentStep == 6) {
		image_parametre.classList.add('active');
    } else {
        image_parametre.classList.remove('active');
	}
}


// Événement : Clic sur Avancer
nextBtn.addEventListener('click', () => {
    if (currentStep < maxSteps) {
        currentStep++;
        updateAnimation();
    }
});

// Événement : Clic sur Reculer
prevBtn.addEventListener('click', () => {
    if (currentStep > 0) {
        currentStep--;
        updateAnimation();
    }
});