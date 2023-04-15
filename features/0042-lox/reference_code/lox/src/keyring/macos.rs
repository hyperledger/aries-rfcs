use security_framework::os::macos::keychain::*;
use security_framework::os::macos::passwords::{SecProtocolType,
                                               SecAuthenticationType,
                                               find_generic_password,
                                               find_internet_password};

use security_framework_sys::item::{SecItemCopyMatching,
                                   kSecReturnAttributes,
                                   kSecMatchLimit,
                                   kSecClass,
                                   kSecClassGenericPassword,
                                   kSecClassInternetPassword,
//                                   kSecClassKey,
//                                   kSecClassCertificate,
//                                   kSecClassIdentity
                                };


use core_foundation::dictionary::{CFDictionaryCreateMutable,
                                  CFMutableDictionaryRef,
                                  CFDictionary,
                                  CFDictionarySetValue, kCFTypeDictionaryKeyCallBacks, kCFTypeDictionaryValueCallBacks};

use core_foundation::base::{CFType,
                            CFTypeRef,
//                            TCFType,
                            CFRelease,
                            kCFAllocatorDefault,
                            FromVoid};
use core_foundation::boolean::kCFBooleanTrue;
use core_foundation::array::CFArray;
use core_foundation::string::CFString;
use core_foundation::number::CFNumber;

use core_foundation_sys::string::CFStringRef;

use std::ffi::c_void;

use crate::parse_peek_criteria;
use crate::base::Result;
use crate::KeyRing;
use crate::KeyRingSecret;
use crate::keyring::get_username;
use std::string::ToString;
use std::collections::BTreeMap;

extern "C" {
    pub static kSecMatchLimitAll: CFStringRef;
}

pub struct MacOsKeyRing {
    keychain: SecKeychain,
    service: String,
}

impl MacOsKeyRing {
    fn unlock(&mut self) -> Result<()>{
        self.keychain.unlock(None).map_err(|e|e.to_string())
    }
    fn get_target_name(&self, id: &str) -> String {
        [get_username(), id.to_string()].join(":")
    }

    fn _find_internet_password(search_criteria: &BTreeMap<String, String>) -> Result<KeyRingSecret> {
        let security_domain = search_criteria.get("security_domain").map(|s|s.as_str());

        let port = parse_port(search_criteria.get("port"));
        let protocol = parse_protocol(&search_criteria["protocol"])?;
        let authentication_type = parse_authentication(&search_criteria["authentication_type"])?;
        let path = search_criteria.get("path").map(|s|s.as_str()).unwrap_or_else(|| "");

        let (pass, _) = find_internet_password(None,
                                               &search_criteria["server"],
                                               security_domain,
                                               &search_criteria["account"],
                                               &path,
                                               port,
                                               protocol,
                                               authentication_type).map_err(|e|e.to_string())?;
        Ok(KeyRingSecret(pass.to_owned()))
    }

    fn _find_generic_password(search_criteria: &BTreeMap<String, String>) -> Result<KeyRingSecret> {
        let (pass, _) = find_generic_password(None, &search_criteria["service"], &search_criteria["account"]).map_err(|e|e.to_string())?;
        Ok(KeyRingSecret(pass.to_owned()))
    }

    fn _find_all_passwords() -> Result<Vec<(String, KeyRingSecret)>> {
        let mut out = Vec::new();

        let mut keychain = SecKeychain::default().map_err(|e|e.to_string())?;
        keychain.unlock(None).map_err(|e|e.to_string())?;

        let secret_names = MacOsKeyRing::list_secrets()?;

        for name in &secret_names {
            match name["kind"].as_str() {
                "generic" => {
                    match keychain.find_generic_password(&name["service"], &name["account"]) {
                        Ok((pass, _)) => out.push((format!("{:?}", name), KeyRingSecret(pass.to_owned()))),
                        Err(e) => {
                            if !out.is_empty() {
                                return Ok(out);
                            } else {
                                return Err(e.to_string());
                            }
                        }
                    }
                },
                "internet" => {
                    let server = &name["server"];
                    let security_domain = None;
                    let account = &name["account"];
                    let path = "";
                    let port = parse_port(Some(&name["port"]));
                    let protocol = parse_protocol(&name["protocol"])?;
                    let authentication_type = parse_authentication(&name["authentication_type"])?;
                    match keychain.find_internet_password(server, security_domain, account, path, port, protocol, authentication_type) {
                        Ok((pass, _)) => out.push((format!("{:?}", name), KeyRingSecret(pass.to_owned()))),
                        Err(e) => {
                            if !out.is_empty() {
                                return Ok(out);
                            } else {
                                return Err(e.to_string());
                            }
                        }
                    }
                }
                _ => ()
            }
        }

        Ok(out)
    }
}

impl KeyRing for MacOsKeyRing {
    fn new(service: &str) -> Result<Self> {
        Ok(MacOsKeyRing{keychain: SecKeychain::default().map_err(|e|e.to_string())?, service: service.to_string()})
    }

    fn get_secret(&mut self, id: &str) -> Result<KeyRingSecret> {
        self.unlock()?;
        let (pass, _) = self.keychain.find_generic_password(&self.service, &self.get_target_name(id)).map_err(|e|e.to_string())?;
        Ok(KeyRingSecret(pass.to_owned()))
    }

    fn list_secrets() -> Result<Vec<BTreeMap<String, String>>> {
        let mut out = Vec::new();
        unsafe {
            let query: CFMutableDictionaryRef = CFDictionaryCreateMutable(kCFAllocatorDefault, 0,
                                                                          &kCFTypeDictionaryKeyCallBacks,
                                                                          &kCFTypeDictionaryValueCallBacks);

            CFDictionarySetValue(query, kSecReturnAttributes as *const c_void, kCFBooleanTrue as *const c_void);
            CFDictionarySetValue(query, kSecMatchLimit as *const c_void, kSecMatchLimitAll as *const c_void);

            let mut types = Vec::new();

            types.push(kSecClassGenericPassword);
            types.push(kSecClassInternetPassword);
//        types.push(kSecClassCertificate);
//        types.push(kSecClassKey);
//        types.push(kSecClassIdentity);

            for i in 0..types.len() {
                CFDictionarySetValue(query, kSecClass as *const c_void, types[i] as *const c_void);
                let mut result: CFTypeRef = std::ptr::null_mut();
                SecItemCopyMatching(query, &mut result);

                let item = CFType::from_void(result);

                let array = item.downcast::<CFArray<*const c_void>>()
                    .unwrap()
                    .get_all_values();

                for j in array {
                    let ty = CFType::from_void(j);
                    let dict = ty.downcast::<CFDictionary<*const c_void, *const c_void>>().unwrap();

                    let (dict_keys, dict_values) = dict.get_keys_and_values();
                    let mut value = BTreeMap::new();

                    for k in 0..dict_keys.len() {
                        let dict_key = keyring_type_to_string(dict_keys[k]);

                        match dict_key.as_str() {
                            "svce" => value.insert("service".to_string(), keyring_type_to_string(dict_values[k])),
                            "acct" => value.insert("account".to_string(), keyring_type_to_string(dict_values[k])),
                            "atyp" => value.insert("authentication_type".to_string(), format!("{:?}", parse_authentication(&keyring_type_to_string(dict_values[k]))?)),
                            "ptcl" => value.insert("protocol".to_string(), format!("{:?}", parse_protocol(&keyring_type_to_string(dict_values[k]))?)),
                            "srvr" => value.insert("server".to_string(), keyring_type_to_string(dict_values[k])),
                            "port" => value.insert("port".to_string(), keyring_type_to_i64(dict_values[k]).to_string()),
                            "class" => value.insert("kind".to_string(), match keyring_type_to_string(dict_values[k]).as_str() {
                                "inet" => "internet".to_string(),
                                "genp" => "generic".to_string(),
                                _ => "".to_string()
                            }),
                            _ => None
                        };
                    }

                    out.push(value);
                }

                CFRelease(result);
            }
        };

        Ok(out)
    }

    fn peek_secret(id: &str) -> Result<Vec<(String, KeyRingSecret)>> {
        if id.is_empty() {
            return MacOsKeyRing::_find_all_passwords();
        }

        let search_criteria = parse_peek_criteria(id);

        if search_criteria.contains_key("kind") {
            match search_criteria["kind"].as_str() {
                "generic" => {
                    if can_find_generic(&search_criteria) {
                        let res = MacOsKeyRing::_find_generic_password(&search_criteria)?;
                        Ok(vec![(id.to_string(), res)])
                    } else {
                        Err("Missing required criteria. 'service' and 'account' must both be supplied".to_string())
                    }
                },
                "internet" => {
                    if can_find_internet(&search_criteria) {
                        let res = MacOsKeyRing::_find_internet_password(&search_criteria)?;
                        Ok(vec![(id.to_string(), res)])
                    } else {
                        Err("Missing required criteria. 'server', 'account', 'path', 'protocol', 'authentication_type' must all be supplied".to_string())
                    }
                },
                _ => Err("Unknown kind provided".to_string())
            }
        } else {
            if can_find_internet(&search_criteria) {
                let res = MacOsKeyRing::_find_internet_password(&search_criteria)?;
                Ok(vec![(id.to_string(), res)])
            } else if can_find_generic(&search_criteria) {
                let res = MacOsKeyRing::_find_generic_password(&search_criteria)?;
                Ok(vec![(id.to_string(), res)])
            } else {
                Err("Can't determine which secret kind to search. 'account' and 'service' or 'account' and 'server', 'path', 'protocol', 'authentication_type' must be supplied".to_string())
            }
        }
    }

    fn set_secret(&mut self, id: &str, secret: &[u8]) -> Result<()> {
        self.unlock()?;
        self.keychain.set_generic_password(&self.service, &self.get_target_name(id), secret).map_err(|e|e.to_string())
    }

    fn delete_secret(&mut self, id: &str) -> Result<()> {
        self.unlock()?;
        let (_,  item) = self.keychain.find_generic_password(&self.service, &self.get_target_name(id)).map_err(|e|e.to_string())?;
        item.delete();
        Ok(())
    }
}

fn keyring_type_to_string(value: *const c_void) -> String {
    let new_value = unsafe { CFType::from_void(value) };
    let value_string = new_value.downcast::<CFString>().unwrap();
    value_string.to_string()
}

fn keyring_type_to_i64(value: *const c_void) -> i64 {
    let new_value = unsafe { CFType::from_void(value) };
    let value_usize = new_value.downcast::<CFNumber>().unwrap();
    match value_usize.to_i64() {
        Some(i) => i,
        None => match value_usize.to_f64() {
            Some(f) => f as i64,
            None => 0
        }
    }
}

fn can_find_generic(criteria: &BTreeMap<String, String>) -> bool {
    criteria.contains_key(&"account".to_string()) &&
    criteria.contains_key(&"service".to_string())
}

fn can_find_internet(criteria: &BTreeMap<String, String>) -> bool {
    let mut result = true;
    for key in &["server", "account", "protocol", "authentication_type"] {
        result &= criteria.contains_key(key.clone());
    }

    if result {
        result &= parse_protocol(&criteria["protocol"]).is_ok();
    }
    if result {
        result &= parse_authentication(&criteria["authentication_type"]).is_ok();
    }

    result
}

fn parse_protocol(value: &str) -> Result<SecProtocolType> {
    match value.to_lowercase().as_str() {
        "ftp" => Ok(SecProtocolType::FTP),
        "ftpa" | "ftpaccount" => Ok(SecProtocolType::FTPAccount),
        "http" => Ok(SecProtocolType::HTTP),
        "irc"  => Ok(SecProtocolType::IRC),
        "nntp" => Ok(SecProtocolType::NNTP),
        "pop3" => Ok(SecProtocolType::POP3),
        "smtp" => Ok(SecProtocolType::SMTP),
        "sox" | "socks"  => Ok(SecProtocolType::SOCKS),
        "imap" => Ok(SecProtocolType::IMAP),
        "ldap" => Ok(SecProtocolType::LDAP),
        "atlk" | "appletalk" => Ok(SecProtocolType::AppleTalk),
        "afp"  => Ok(SecProtocolType::AFP),
        "teln" | "telnet" => Ok(SecProtocolType::Telnet),
        "ssh"  => Ok(SecProtocolType::SSH),
        "ftps" => Ok(SecProtocolType::FTPS),
        "htps" | "https" => Ok(SecProtocolType::HTTPS),
        "htpx" | "httpproxy" => Ok(SecProtocolType::HTTPProxy),
        "htsx" | "httpsproxy" => Ok(SecProtocolType::HTTPSProxy),
        "ftpx" | "ftpproxy" => Ok(SecProtocolType::FTPProxy),
        "cifs" => Ok(SecProtocolType::CIFS),
        "smb"  => Ok(SecProtocolType::SMB),
        "rtsp" => Ok(SecProtocolType::RTSP),
        "rtsx" | "rtspproxy" => Ok(SecProtocolType::RTSPProxy),
        "daap" => Ok(SecProtocolType::DAAP),
        "eppc" => Ok(SecProtocolType::EPPC),
        "ipp"  => Ok(SecProtocolType::IPP),
        "ntps" | "nntps" => Ok(SecProtocolType::NNTPS),
        "ldps" | "ldaps" => Ok(SecProtocolType::LDAPS),
        "tels" | "telnets" => Ok(SecProtocolType::TelnetS),
        "imps" | "imaps" => Ok(SecProtocolType::IMAPS),
        "ircs" => Ok(SecProtocolType::IRCS),
        "pops" | "pop3s" => Ok(SecProtocolType::POP3S),
        "cvsp" | "cvspserver" => Ok(SecProtocolType::CVSpserver),
        "svn"  => Ok(SecProtocolType::SVN),
        ""     => Ok(SecProtocolType::Any),
        _ => Err("No matching protocol found".to_string())
    }
}

fn parse_authentication(value: &str) -> Result<SecAuthenticationType> {
    match value.to_lowercase().as_str() {
        "ntlm" => Ok(SecAuthenticationType::NTLM),
        "msna" => Ok(SecAuthenticationType::MSN),
        "dpaa" => Ok(SecAuthenticationType::DPA),
        "rpaa" => Ok(SecAuthenticationType::RPA),
        "http" | "httpbasic" => Ok(SecAuthenticationType::HTTPBasic),
        "httd" | "httpdigest"=> Ok(SecAuthenticationType::HTTPDigest),
        "form" | "htmlform" => Ok(SecAuthenticationType::HTMLForm),
        "dflt" | "default" => Ok(SecAuthenticationType::Default),
        ""     => Ok(SecAuthenticationType::Any),
        _      => Err("No matching authentication type found".to_string())
    }
}

fn parse_port(value: Option<&String>) -> Option<u16> {
    match value {
        Some(p) => match p.parse::<u16>() {
            Ok(i) => if i > 0 {
                Some(i)
            } else {
                None
            },
            Err(_) => None
        },
        None => None
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_port_test() {
        assert!(parse_port(Some(&"-1".to_string())).is_none());
        assert!(parse_port(Some(&"0".to_string())).is_none());
        assert!(parse_port(Some(&"65535".to_string())).is_some());
        assert!(parse_port(Some(&"1034124".to_string())).is_none());
        assert!(parse_port(None).is_none());
    }

    #[test]
    fn parse_protocol_test() {
        assert!(parse_protocol("mysql").is_err());
        assert!(parse_protocol("ftp").is_ok());
    }
}
