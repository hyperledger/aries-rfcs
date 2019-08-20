#[cfg(target_os = "linux")]
pub mod linux;
#[cfg(target_os = "macos")]
pub mod macos;
#[cfg(target_os = "windows")]
pub mod windows;

#[cfg(target_os = "macos")]
pub(crate) use self::macos::MacOsKeyRing as OsKeyRing;

#[cfg(target_os = "linux")]
pub(crate) use self::linux::LinuxOsKeyRing as OsKeyRing;

#[cfg(target_os = "windows")]
pub(crate) use self::windows::WindowsOsKeyRing as OsKeyRing;

use crate::base::Result;
use crate::KeyRing;
#[cfg(any(
    target_os = "linux",
    target_os = "macos"
))]
use users::{get_effective_username, get_current_username};

pub fn get_os_keyring(service: &str) -> Result<OsKeyRing> {
    OsKeyRing::new(service)
}

#[cfg(not(any(
    target_os = "linux",
    target_os = "macos",
    target_os = "windows"
)))]
compile_error!("no keyring implementation is available for this platform");


#[cfg(any(
    target_os = "linux",
    target_os = "macos"
))]
fn get_username() -> String {
    fn get_current_user() -> String {
        match get_current_username() {
            Some(s) => match s.into_string() {
                Ok(r) => r,
                Err(_) => whoami::username()
            },
            None => whoami::username()
        }
    }

    match get_effective_username() {
        Some(s) => {
            match s.into_string() {
                Ok(r) => r,
                Err(_) => get_current_user()
            }
        },
        None => get_current_user()
    }
}
