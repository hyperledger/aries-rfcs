use secret_service::{EncryptionType, SecretService};

use crate::base::Result;
use crate::keyring::get_username;
use crate::KeyRing;
use crate::KeyRingSecret;
use crate::parse_peek_criteria;

use std::collections::BTreeMap;

pub struct LinuxOsKeyRing {
    keychain: SecretService,
    service: String,
    username: String,
}

impl KeyRing for LinuxOsKeyRing {
    fn new(service: &str) -> Result<Self> {
        Ok(LinuxOsKeyRing {
            keychain: SecretService::new(EncryptionType::Dh).map_err(|e| e.to_string())?,
            service: service.to_string(),
            username: get_username()
        })
    }

    fn get_secret(&mut self, id: &str) -> Result<KeyRingSecret> {
        let collection = self.keychain.get_default_collection().map_err(|e| e.to_string())?;
        if collection.is_locked().map_err(|e|e.to_string())? {
            collection.unlock().map_err(|e| e.to_string())?
        }
        let attributes = vec![
                ("application", "lox"),
                ("service", &self.service),
                ("username", &self.username),
                ("id", id)
            ];
        let search = collection.search_items(attributes).map_err(|e| e.to_string())?;
        let item = search.get(0).ok_or_else(|| "No secret found".to_string())?;
        let secret = item.get_secret().map_err(|e| e.to_string())?;
        Ok(KeyRingSecret(secret))
    }

    fn list_secrets() -> Result<Vec<BTreeMap<String, String>>> {
        let key_chain = SecretService::new(EncryptionType::Dh).map_err(|e| e.to_string())?;
        let collection = key_chain.get_default_collection().map_err(|e|e.to_string())?;
        if collection.is_locked().map_err(|e|e.to_string())? {
            collection.unlock().map_err(|e| e.to_string())?
        }
        let items = collection.get_all_items().map_err(|e|e.to_string())?;
        let mut out = Vec::new();
        for item in &items {
            match item.get_attributes() {
                Ok(atts) => {
                    out.push(vec_to_btreemap(atts));
                },
                Err(e) => {
                    if !out.is_empty() {
                        return Ok(out)
                    } else {
                        return Err(e.to_string())
                    }
                }
            }
        }

        Ok(out)
    }

    fn peek_secret(id: &str) -> Result<Vec<(String, KeyRingSecret)>> {
        let key_chain = SecretService::new(EncryptionType::Dh).map_err(|e| e.to_string())?;
        let collection = key_chain.get_default_collection().map_err(|e|e.to_string())?;
        if collection.is_locked().map_err(|e|e.to_string())? {
            collection.unlock().map_err(|e| e.to_string())?
        }
        let attributes = parse_peek_criteria(id);

        let items = collection.get_all_items().map_err(|e|e.to_string())?;
        let mut out = Vec::new();

        for item in &items {
            match item.get_attributes() {
                Ok(atts) => {
                    let mut matches = true;
                    let filter = vec_to_btreemap(atts);
                    for (k, v) in &attributes {
                        if filter.contains_key(k) {
                            matches = filter[k] == v.as_str();
                        } else {
                            matches = false;
                        }
                        if !matches { break; }
                    }
                    if matches || id.is_empty() {
                        let secret = item.get_secret().map_err(|e| e.to_string())?;
                        out.push((format!("{:?}", filter), KeyRingSecret(secret)));
                    }
                },
                Err(e) => {
                    if !out.is_empty() {
                        return Ok(out)
                    } else {
                        return Err(e.to_string())
                    }
                }
            }
        }

        Ok(out)
    }

    fn set_secret(&mut self, id: &str, secret: &[u8]) -> Result<()> {
        let collection = self.keychain.get_default_collection().map_err(|e| e.to_string())?;
        if collection.is_locked().map_err(|e|e.to_string())? {
            collection.unlock().map_err(|e| e.to_string())?
        }
        let attributes = vec![
                ("application", "lox"),
                ("service", &self.service),
                ("username", &self.username),
                ("id", id)
            ];
        collection.create_item(&format!("Secret for {}", id), attributes, secret, true, "text/plain").map_err(|e| e.to_string())?;
        Ok(())
    }

    fn delete_secret(&mut self, id: &str) -> Result<()> {
        let collection = self.keychain.get_default_collection().map_err(|e| e.to_string())?;
        if collection.is_locked().map_err(|e|e.to_string())? {
            collection.unlock().map_err(|e| e.to_string())?
        }
        let attributes = vec![
                ("application", "lox"),
                ("service", &self.service),
                ("username", &self.username),
                ("id", id)
            ];
        let search = collection.search_items(attributes).map_err(|e| e.to_string())?;
        let item = search.get(0).ok_or_else(|| "No secret found".to_string())?;
        item.delete().map_err(|e| e.to_string())
    }
}

fn vec_to_btreemap(values: Vec<(String, String)>) -> BTreeMap<String, String> {
    let mut value = BTreeMap::new();
    for (k, v) in values {
        value.insert(k.to_string(), v.to_string());
    }
    value
}
