use crate::base::Result;
use super::super::KeyRing;
use super::super::KeyRingSecret;

use byteorder::LittleEndian;
use crate::byteorder::ByteOrder;
use std::os::windows::ffi::{OsStrExt, OsStringExt};
use std::ffi::{OsStr, OsString};
use std::iter::once;

use winapi::ctypes::c_void;

use winapi::shared::minwindef::FILETIME;
use winapi::shared::winerror::{ERROR_NOT_FOUND, ERROR_NO_SUCH_LOGON_SESSION, ERROR_INVALID_FLAGS};
use winapi::um::errhandlingapi::GetLastError;
use winapi::um::winbase::LocalFree;
use winapi::um::dpapi::{
    CryptProtectData,
    CryptUnprotectData,
};
use winapi::um::wincred::{
    CredReadW,
    CredWriteW,
    CredDeleteW,
    CredEnumerateW,
    CredFree,
    PCREDENTIAL_ATTRIBUTEW,
    PCREDENTIALW,
    CREDENTIALW,
    CRED_TYPE_GENERIC,
    CRED_PERSIST_ENTERPRISE,
    CRED_ENUMERATE_ALL_CREDENTIALS
};
use winapi::um::wincrypt::{CRYPTOAPI_BLOB, PDATA_BLOB};
use zeroize::Zeroize;
use std::collections::BTreeMap;
//use generic_array::functional::FunctionalSequence;


pub struct WindowsOsKeyRing {
    service: String,
    username: String,
}

impl WindowsOsKeyRing {
    fn get_target_name(&self, id: &str) -> Vec<u16> {
        let target_name = [&self.username, &self.service, id].join(":");
        to_utf16_bytes(&target_name)
    }

    fn handle_err<T>() -> Result<T> {
        match unsafe { GetLastError() } {
            ERROR_NOT_FOUND => Err("The specified item could not be found in the keychain.".to_string()),
            ERROR_NO_SUCH_LOGON_SESSION => Err("The logon session does not exist or there is no credential set associated with this logon session.".to_string()),
            ERROR_INVALID_FLAGS => Err("A flag that is not valid was specified for the Flags parameter, or CRED_ENUMERATE_ALL_CREDENTIALS is specified for the Flags parameter and the Filter parameter is not NULL.".to_string()),
            _ => Err("Windows Vault Error.".to_string())
        }
    }
}

impl KeyRing for WindowsOsKeyRing {
    fn new(service: &str) -> Result<Self> {
        Ok(WindowsOsKeyRing { service: service.to_string(), username: whoami::username() })
    }

    fn get_secret(&mut self, id: &str) -> Result<KeyRingSecret> {
        let mut target_name = self.get_target_name(id);
        let mut pcredential: PCREDENTIALW = std::ptr::null_mut();

        let cred_type = CRED_TYPE_GENERIC;
        let res = unsafe { CredReadW(target_name.as_ptr(), cred_type, 0, &mut pcredential) };

        if res == 0 {
            return WindowsOsKeyRing::handle_err::<KeyRingSecret>();
        }

        let credential: CREDENTIALW = unsafe { *pcredential };

        let mut in_blob = CRYPTOAPI_BLOB {
            cbData: credential.CredentialBlobSize, pbData: credential.CredentialBlob
        };
        let in_blob_ptr: PDATA_BLOB = &mut in_blob;

        let mut out_blob = CRYPTOAPI_BLOB {
            cbData: 0, pbData: std::ptr::null_mut()
        };
        let out_blob_ptr: PDATA_BLOB = &mut out_blob;

        let descr = &mut target_name.as_mut_ptr();

        let res = match unsafe { CryptUnprotectData(
            in_blob_ptr,
            descr,
            std::ptr::null_mut(),
            std::ptr::null_mut(),
            std::ptr::null_mut(),
            0,
            out_blob_ptr
        ) } {
            0 => Err("Windows Crypt Unprotect Data Error".to_string()),
            _ => {
                //TODO: figure out how to zero pbData after its loaded into the KeyRingSecret
                let secret = unsafe { std::slice::from_raw_parts_mut(out_blob.pbData, out_blob.cbData as usize) };
                let r = Ok(KeyRingSecret(secret.to_vec()));
                secret.zeroize();
                r
            }
        };
        unsafe { CredFree(pcredential as *mut c_void) };
        unsafe { LocalFree(out_blob.pbData as *mut c_void) };
        res
    }

    fn list_secrets() -> Result<Vec<BTreeMap<String, String>>> {
        let filter = std::ptr::null();
        let flags = CRED_ENUMERATE_ALL_CREDENTIALS;
        let mut pcredentials: *mut PCREDENTIALW = std::ptr::null_mut();
        let mut count = 0;

        let res = unsafe { CredEnumerateW(filter, flags, &mut count, &mut pcredentials) };
         if res == 0 {
            return WindowsOsKeyRing::handle_err::<Vec<BTreeMap<String, String>>>();
        }

        let credentials: &[PCREDENTIALW] = unsafe { std::slice::from_raw_parts_mut(pcredentials, count as usize) };

        let mut found_credentials = Vec::new();

        for c in credentials {
            let cred: CREDENTIALW = unsafe { **c };
            let mut i = 0isize;
            while unsafe { *cred.TargetName.offset(i) } != 0u16 {
                i += 1;
            }
            let target = unsafe { std::slice::from_raw_parts(cred.TargetName, i as usize) };
            let name = OsString::from_wide(target).into_string().unwrap();
            let mut value = BTreeMap::new();
            value.insert("targetname".to_string(), name);

            found_credentials.push(value);
        }
        unsafe { CredFree(pcredentials as *mut c_void) };
        Ok(found_credentials)
    }

    fn peek_secret(id: &str) -> Result<Vec<(String, KeyRingSecret)>> {
        let flags = if id.is_empty() {
                            CRED_ENUMERATE_ALL_CREDENTIALS
                        } else {
                            0
                        };

        let found_credentials = unsafe { get_credentials(id, flags)? };

        Ok(found_credentials)
    }

    fn set_secret(&mut self, id: &str, secret: &[u8]) -> Result<()> {
        let mut target_name = self.get_target_name(id);
        let mut empty = to_utf16_bytes("");
        let attributes: PCREDENTIAL_ATTRIBUTEW = std::ptr::null_mut();
        let mut user_name = to_utf16_bytes(&self.username);
        let persist = CRED_PERSIST_ENTERPRISE;
        let mut secret_cp = secret.to_vec();

        let mut in_blob = CRYPTOAPI_BLOB {
            cbData: secret.len() as u32, pbData: secret_cp.as_mut_ptr()
        };
        let in_blob_ptr: PDATA_BLOB = &mut in_blob;
        let mut out_blob = CRYPTOAPI_BLOB {
            cbData: 0, pbData: std::ptr::null_mut()
        };
        let out_blob_ptr: PDATA_BLOB = &mut out_blob;

        let res = unsafe { CryptProtectData(in_blob_ptr,
                                        target_name.as_mut_ptr(),
                                        std::ptr::null_mut(),
                                            std::ptr::null_mut(),
                                        std::ptr::null_mut(),
                                        0,
                                        out_blob_ptr) };
        if res == 0 {
            return Err("Windows Crypt Protect Data Error".to_string());
        }

        secret_cp.zeroize();

        let mut credential = CREDENTIALW {
            Flags: 0,
            Type: CRED_TYPE_GENERIC,
            TargetName: target_name.as_mut_ptr(),
            Comment: empty.as_mut_ptr(),
            LastWritten: FILETIME { dwHighDateTime: 0, dwLowDateTime: 0 },
            CredentialBlobSize: out_blob.cbData,
            CredentialBlob: out_blob.pbData,
            Persist: persist,
            Attributes: attributes,
            AttributeCount: 0,
            TargetAlias: empty.as_mut_ptr(),
            UserName: user_name.as_mut_ptr()
        };
        let pcredential: PCREDENTIALW = &mut credential;
        let res = match unsafe { CredWriteW(pcredential, 0) } {
            0 => Err("Windows Vault Error".to_string()),
            _ => Ok(())
        };
        unsafe { LocalFree(out_blob.pbData as *mut c_void) };
        res
    }

    fn delete_secret(&mut self, id: &str) -> Result<()> {
        let target_name = self.get_target_name(id);

        match unsafe { CredDeleteW(target_name.as_ptr(), CRED_TYPE_GENERIC, 0) } {
            0 => WindowsOsKeyRing::handle_err::<()>(),
            _ => Ok(())
        }
    }
}

fn to_utf16_bytes(s: &str) -> Vec<u16> {
    OsStr::new(s).encode_wide().chain(once(0)).collect()
}

unsafe fn get_credentials(id: &str, flags: u32) -> Result<Vec<(String, KeyRingSecret)>> {
    let id = if !id.is_empty() {
        to_utf16_bytes(id)
    } else {
        Vec::new()
    };
    let filter = if flags > 0 {
        std::ptr::null()
    } else {
        id.as_ptr()
    };
    let mut pcredentials: *mut PCREDENTIALW = std::ptr::null_mut();
    let mut count = 0;
    let res = CredEnumerateW(filter, flags, &mut count, &mut pcredentials);
     if res == 0 {
        return WindowsOsKeyRing::handle_err::<Vec<(String, KeyRingSecret)>>();
    }

    let credentials: &[PCREDENTIALW] = std::slice::from_raw_parts_mut(pcredentials, count as usize);

    let mut found_credentials = Vec::new();

    for c in credentials {
        let cred: CREDENTIALW = **c;
        let blob: *const u8 = cred.CredentialBlob;
        let blob_len: usize = cred.CredentialBlobSize as usize;
        let mut i = 0isize;
        while *cred.TargetName.offset(i) != 0u16 {
            i += 1;
        }
        let target = std::slice::from_raw_parts(cred.TargetName, i as usize);
        let name = OsString::from_wide(target).into_string().unwrap();

        let secret = std::slice::from_raw_parts(blob, blob_len);
        let mut secret_u16 = vec![0; blob_len / 2];
        LittleEndian::read_u16_into(&secret, &mut secret_u16);
        let t = match String::from_utf16(secret_u16.as_slice()).map(|pass|pass.to_string()) {
            Ok(s) => s,
            Err(_) => {
                match String::from_utf8(secret.to_vec()).map(|pass|pass.to_string()) {
                    Ok(s1) => s1,
                    Err(_) => {
                        //Binary blob
                        secret.iter()
                              .map(|b| format!("{:02x}", b))
                              .collect::<Vec<_>>()
                              .join("")
                    }
                }
            }
        };
        found_credentials.push((name, KeyRingSecret(t.as_bytes().to_vec())));
    }
    CredFree(pcredentials as *mut c_void);
    Ok(found_credentials)
}
