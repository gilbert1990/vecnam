// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;
pragma experimental ABIEncoderV2;

// A library is like a contract with reusable code, which can be called by other contracts.
// Deploying common code can reduce gas costs.
contract ManagementUser {
    enum Rol {
        admin,
        doctor,
        patient
    }
    enum Opciones {
        Nunca,
        Ocasionalmete,
        Frecuetemente
    }
    enum Affirmations {
        Si,
        No
    }
    enum Estatus {
        pendientes,
        programadas
    }
    /* Antecedentes personales*/
    struct MedicalHistory {
        Opciones alcohol;
        Opciones smoke;
        Opciones physical_activity;
        Opciones contraceptives;
        Affirmations fracture;
        string surgery;
    }
    /* Antecedentes familiares*/
    struct FamilyHistory {
        Affirmations diabetes;
        Affirmations hypertension;
        Affirmations heart;
        Affirmations respiratory;
        Affirmations alzheimer;
        Affirmations cardiovascular;
        Affirmations cancer;
    }

    struct User {
        string name;
        string birthdate;
        int document;
        string date_document;
        string email;
        Rol role;
        string passwordHash;
        bool isAuthenticated; // Nuevo campo para el estado de autenticación
        address medicalHistoryAddress; // Dirección para acceder a los antecedentes médicos
        address familyHistoryAddress; // Dirección para acceder a los antecedentes familiares
    }
    User[] public usuariosRegistrados; // Lista de direcciones de usuarios registrados

    // Mapping para comprobar si un número de documento ya existe
    mapping(int => bool) public documentExists;
    // Mapeo de documentos a direcciones
    mapping(int => address) public documentToAddress;
    mapping(address => MedicalHistory) public medicalHistories;
    mapping(address => FamilyHistory) public familyHistories;
    mapping(address => User) public users;
    mapping(address => bool) public isUser;

    event UserAuthenticated(address indexed userAddress, int document);
    event NewUser(
        address indexed _address,
        string _name,
        int _document,
        string _expedition_documente,
        Rol _role,
        string _passwordHash,
        bool _isAuthenticated
    );

    /* Crea el usuario */
    function createUser(
        string memory _name,
        string memory _birthdate,
        int _document,
        string memory _date_document,
        string memory _email,
        Rol _role,
        string memory _passwordHash
    ) public {
        require(!documentExists[_document], "El usuario ya existe");
        // Crear una instancia de antecedentes médicos vacía y vincularla al usuario
        MedicalHistory memory emptyMedicalHistory;
        address medicalHistoryAddress = address(
            bytes20(keccak256(abi.encodePacked(msg.sender, block.timestamp)))
        );
        medicalHistories[medicalHistoryAddress] = emptyMedicalHistory;
        // Crear una instancia de antecedentes familia vacía y vincularla al usuario
        FamilyHistory memory emptyFamilyHistory;
        address familyHistoryAddress = address(
            bytes20(keccak256(abi.encodePacked(msg.sender)))
        );
        familyHistories[familyHistoryAddress] = emptyFamilyHistory;

        //Guardar usuario
        users[msg.sender] = User(
            _name,
            _birthdate,
            _document,
            _date_document,
            _email,
            _role,
            _passwordHash,
            false,
            medicalHistoryAddress,
            familyHistoryAddress
        );
        isUser[msg.sender] = true;
        documentExists[_document] = true;
        documentToAddress[_document] = msg.sender;
        usuariosRegistrados.push(users[msg.sender]);
        emit NewUser(
            msg.sender,
            _name,
            _document,
            _date_document,
            _role,
            _passwordHash,
            false
        );
    }

    // Autenticar al usuario
    function authenticateUser(
        int _document,
        string memory _password,
        Rol _role
    ) public {
        User storage user = users[msg.sender];
        require(isUser[msg.sender], "El usuario no existe");
        require(user.document == _document, "Documento incorrecto"); // Comprueba el documento
        require(user.role == _role, "Rol incorrecto"); // Comprueba el rol del usuario

        // Comparar el hash de la contraseña ingresada con el hash almacenado
        require(
            keccak256(abi.encodePacked(_password)) ==
                keccak256(abi.encodePacked(user.passwordHash)),
            "Contrasena incorrecta"
        );

        user.isAuthenticated = true;
        emit UserAuthenticated(msg.sender, user.document);
    }

    function setFamilyHistory(
        Affirmations diabetes,
        Affirmations hypertension,
        Affirmations heart,
        Affirmations respiratory,
        Affirmations alzheimer,
        Affirmations cardiovascular,
        Affirmations cancer,
        address familyHistoryAddress
    ) public {
        // Accede a los antecedentes médicos del usuario actual
        FamilyHistory storage userFamilyHistory = familyHistories[
            familyHistoryAddress
        ];

        userFamilyHistory.diabetes = diabetes;
        userFamilyHistory.hypertension = hypertension;
        userFamilyHistory.heart = heart;
        userFamilyHistory.respiratory = respiratory;
        userFamilyHistory.alzheimer = alzheimer;
        userFamilyHistory.cardiovascular = cardiovascular;
        userFamilyHistory.cancer = cancer;

        // Actualiza los antecedentes médicos en el contrato
        familyHistories[familyHistoryAddress] = userFamilyHistory;
    }

    function setMedicalHistory(
        Opciones alcohol,
        Opciones smoke,
        Opciones physical_activity,
        Opciones contraceptives,
        Affirmations fracture,
        string memory surgery,
        address medicalHistoryAddress
    ) public {
        // Accede a los antecedentes médicos del usuario actual
        MedicalHistory storage userMedicalHistory = medicalHistories[
            medicalHistoryAddress
        ];

        userMedicalHistory.alcohol = alcohol;
        userMedicalHistory.smoke = smoke;
        userMedicalHistory.physical_activity = physical_activity;
        userMedicalHistory.contraceptives = contraceptives;
        userMedicalHistory.fracture = fracture;
        userMedicalHistory.surgery = surgery;

        // Actualiza los antecedentes médicos en el contrato
        medicalHistories[medicalHistoryAddress] = userMedicalHistory;
    }

    function getFamilyHistoryAddress(
        address familyHistoryAddress
    ) public view returns (FamilyHistory memory) {
        return familyHistories[familyHistoryAddress];
    }

    function getMedicalHistoryAddress(
        address medicalHistoryAddress
    ) public view returns (MedicalHistory memory) {
        return medicalHistories[medicalHistoryAddress];
    }

    /* Consulta todos los nombre de los usuarios */
    function getAllUserNames() public view returns (User[] memory) {
        return usuariosRegistrados;
    }

    function isUserAuthenticated() public view returns (bool) {
        return users[msg.sender].isAuthenticated;
    }

    // Función para consultar información de un usuario por documento
    function getUserInfoByDocument(
        int document
    ) public view returns (User memory) {
        address userAddress = documentToAddress[document];
        require(userAddress != address(0), "Usuario no encontrado");
        User memory user = users[userAddress];
        return user;
    }
}
