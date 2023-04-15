#![deny(
    warnings,
    unused_import_braces,
    unused_qualifications,
    trivial_casts,
    trivial_numeric_casts
)]

#[cfg(target_os = "macos")]
extern crate security_framework;
#[cfg(target_os = "macos")]
extern crate security_framework_sys;
#[cfg(target_os = "macos")]
extern crate core_foundation;
#[cfg(target_os = "macos")]
extern crate core_foundation_sys;
#[cfg(target_os = "linux")]
extern crate secret_service;
#[cfg(target_os = "windows")]
extern crate winapi;
#[cfg(target_os = "windows")]
extern crate byteorder;
#[cfg(any(target_os = "macos", target_os="linux"))]
extern crate users;

#[cfg(any(target_os = "macos", target_os = "linux"))]
use std::collections::BTreeMap;
use zeroize::Zeroize;

pub mod base {
    pub type Result<T> = std::result::Result<T, String>;
}

pub trait KeyRing: Sized {
    fn new(service: &str) -> base::Result<Self>;

    fn get_secret(&mut self, id: &str) -> base::Result<KeyRingSecret>;

    fn set_secret(&mut self, id: &str, secret: &[u8]) -> base::Result<()>;

    fn delete_secret(&mut self, id: &str) -> base::Result<()>;

    fn peek_secret(id: &str) -> base::Result<Vec<(String, KeyRingSecret)>>;

    fn list_secrets() -> base::Result<Vec<BTreeMap<String, String>>>;
}

#[derive(Zeroize)]
#[zeroize(drop)]
pub struct KeyRingSecret(Vec<u8>);

impl KeyRingSecret {
    pub fn as_slice(&self) -> &[u8] {
        self.0.as_slice()
    }

    pub fn to_vec(&self) -> Vec<u8> {
        self.0.to_vec()
    }
}

pub mod keyring;

#[cfg(any(target_os = "macos", target_os = "linux"))]
fn parse_peek_criteria(id: &str) -> BTreeMap<String, String> {
    let mut result = BTreeMap::new();
    if !id.is_empty() {
        for pair in id.split(",") {
            let s = pair.split("=").collect::<Vec<&str>>();
            result.insert(s[0].to_string(), s[1].to_string());
        }
    }
    result
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn parse_peek_criteria_test() {
        for pair in &[("", 0), ("kind=generic", 1), ("kind=internet,account=aws", 2), ("account=aws,service=lox", 2)] {
            let criteria = parse_peek_criteria(pair.0);
            assert_eq!(criteria.len(), pair.1);
        }
    }
}
