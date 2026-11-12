package com.mkii.coursemanagementsystem.service;

import com.mkii.coursemanagementsystem.dto.DecryptRequestDTO;
import com.mkii.coursemanagementsystem.dto.DecryptResponseDTO;
import com.mkii.coursemanagementsystem.dto.EncryptRequestDTO;
import com.mkii.coursemanagementsystem.dto.EncryptResponseDTO;

public interface SecurityService {

    /**
     * Encrypts plaintext string using AES CBC mode with random IV.
     */
    EncryptResponseDTO encrypt(EncryptRequestDTO request);

    /**
     * Decrypts Base64 ciphertext with prepended IV back to original plaintext.
     */
    DecryptResponseDTO decrypt(DecryptRequestDTO request);
}
