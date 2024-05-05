document.addEventListener('DOMContentLoaded', () => {
    // Initialiser avec un nombre défini de personnages, ajustez ce nombre selon vos besoins
    updateCharacterList(8);
    document.getElementById('startButton').addEventListener('click', sendDataToPython);
    document.getElementById('saveButton').addEventListener('click', function() {
        const configName = prompt("Please enter the name for the configuration file:");
        if (configName) {
            eel.save_keys_to_file(configName)((response) => {
                alert(response);  // Affiche une réponse de la sauvegarde
            });
        } else {
            alert("Save cancelled: No name provided.");
        }
    });
});

function saveKeys() {
    eel.save_keys_to_file((response) => {
        alert(response); // Affiche une alerte avec la réponse du serveur
    });
}

function sendDataToPython() {
    const listItems = document.querySelectorAll('#characterList li');
    const characters = [];
    const characterKeyMapping = {};  // Dictionnaire pour les noms et les touches

    listItems.forEach((item, index) => {
        const nameInput = item.querySelector(`input[name='characterName${index + 1}']`);
        const keyInput = item.querySelector(`input[name='characterTouche${index + 1}']`);
        if (nameInput && keyInput && nameInput.value && keyInput.value) {
            characters.push({
                name: nameInput.value,
                key: keyInput.value
            });
            characterKeyMapping[nameInput.value] = keyInput.value;  // Ajouter au dictionnaire
        }
    });

    if (characters.length > 0) {
        eel.assign_keys_to_windows(characters)((window_keys) => {
            console.log('Windows keys assigned:', window_keys);
            console.log('Character to key mapping:', characterKeyMapping);
            document.getElementById('saveButton').style.display = 'block';  // Rendre le bouton visible
        });
    } else {
        alert("No data to input.");
    }
    eel.assign_keys_to_windows(characters)((window_keys) => {
        console.log('Windows keys assigned:', window_keys);
        document.getElementById('saveButton').style.display = 'block';  // Rendre le bouton visible
    });
}

function updateCharacterList(count) {
    const list = document.getElementById('characterList');
    list.innerHTML = ''; // Effacer la liste actuelle
    for (let i = 1; i <= count; i++) {
        const item = document.createElement('li');

        const input = document.createElement('input');
        input.type = 'text';
        input.name = 'characterName' + i;
        input.placeholder = 'Nom du personnage ' + i;

        const touche = document.createElement('input');
        touche.type = 'text';
        touche.name = 'characterTouche' + i;
        touche.placeholder = 'Choisissez une touche';
        touche.readOnly = true; // Empêcher la saisie manuelle

        touche.addEventListener('keydown', function(event) {
            event.preventDefault(); // Empêche le comportement par défaut pour toutes les touches
        
            // Gérer la touche Backspace séparément
            if (event.key === 'Backspace') {
                this.value = ''; // Efface le contenu si Backspace est pressé
                return; // Sortir de la fonction pour ne pas traiter d'autres logiques
            }
        
            // Initialiser la description de la combinaison de touches
            let keyDescription = '';
        
            // Vérifier et ajouter des modificateurs à la description si pressés
            if (event.altKey) keyDescription += 'Alt+';
            if (event.ctrlKey) keyDescription += 'Ctrl+';
            if (event.shiftKey) keyDescription += 'Shift+';
        
            // Ajouter la touche principale à la description, sauf pour les modificateurs seuls
            if (!event.key.match(/Control|Alt|Shift/)) {
                keyDescription += event.key;
            }
        
            // Mettre à jour la valeur de l'input avec la description de la combinaison de touches
            this.value = keyDescription;
        });
        
        item.appendChild(input);
        item.appendChild(touche);
        list.appendChild(item);
    }
}

function loadConfiguration(input) {
    const file = input.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const config = JSON.parse(e.target.result);
            updateCharacterListWithConfig(config);
        };
        reader.readAsText(file); // Lire le fichier comme texte
    }
}

function updateCharacterListWithConfig(config) {
    const list = document.getElementById('characterList');
    list.innerHTML = ''; // Nettoyer la liste existante
    Object.entries(config).forEach(([name, key], index) => {
        const item = document.createElement('li');
        
        const input = document.createElement('input');
        input.type = 'text';
        input.name = `characterName${index + 1}`;
        input.value = name; // Pré-remplir avec le nom du personnage

        const touche = document.createElement('input');
        touche.type = 'text';
        touche.name = `characterTouche${index + 1}`;
        touche.value = key; // Pré-remplir avec la touche
        touche.readOnly = true; // Pour empêcher la modification directe, facultatif

        item.appendChild(input);
        item.appendChild(touche);
        list.appendChild(item);
    });
}
