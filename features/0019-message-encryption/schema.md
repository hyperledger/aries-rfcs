# Schema
This spec is according [JSON Schema v0.7](https://json-schema.org/specification.html)
```json
{
    "id": "https://github.com/hyperledger/indy-agent/wiremessage.json",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Json Web Message format",
    "type": "object",
    "required": ["ciphertext", "iv", "protected", "tag"],
    "properties": {
        "protected": {
            "type": "object",
            "description": "Additional authenticated message data base64URL encoded, so it can be verified by the recipient using the tag",
            "required": ["enc", "typ", "alg", "recipients"],
            "properties": {
                "enc": {
                    "type": "string",
                    "enum": ["xchacha20poly1305_ietf"],
                    "description": "The authenticated encryption algorithm used to encrypt the ciphertext"
                },
                "typ": { 
                    "type": "string",
                    "description": "The message type. Ex: JWM/1.0"
                },
                "alg": {
                    "type": "string",
                    "enum": [ "authcrypt", "anoncrypt"]
                },
                "recipients": {
                    "type": "array",
                    "description": "A list of the recipients who the message is encrypted for",
                    "items": {
                        "type": "object",
                        "required": ["encrypted_key", "header"],
                        "properties": {
                            "encrypted_key": {
                                "type": "string",
                                "description": "The key used for encrypting the ciphertext. This is also referred to as a cek"
                            },
                            "header": {
                                "type": "object",
                                "required": ["kid"],
                                "description": "The recipient to whom this message will be sent",
                                "properties": {
                                    "kid": {
                                        "type": "string",
                                        "description": "base58 encoded verkey of the recipient."
                                    }
                                }
                            }
                        }
                    }
                 },     
            },
        },
        "iv": {
            "type": "string",
            "description": "base64 URL encoded nonce used to encrypt ciphertext"
        },
        "ciphertext": {
            "type": "string",
            "description": "base64 URL encoded authenticated encrypted message"
        },
        "tag": {
            "type": "string",
            "description": "Integrity checksum/tag base64URL encoded to check ciphertext, protected, and iv"
        }
    }
}
```