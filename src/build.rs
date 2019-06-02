use cmake;

fn main() {
    #[cfg(feature = "no_bssl")]
    return;

    let bssl_dir = std::env::var("QUICHE_BSSL_PATH").unwrap_or_else(|_| {
        cmake::Config::new("deps/boringssl")
            .cflag("-fPIC")
            .build_target("bssl")
            .build()
            .display()
            .to_string()
    });

    // MSVC generator on Windows place static libs in a target sub-folder,
    // so adjust library location based on platform and build target.
    // See issue: https://github.com/alexcrichton/cmake-rs/issues/18
    let crypto_dir = if cfg!(windows) {
        if cfg!(debug_assertions) {
            format!("{}/build/crypto/Debug", bssl_dir)
        } else {
            format!("{}/build/crypto/RelWithDebInfo", bssl_dir)
        }
    } else {
        format!("{}/build/crypto", bssl_dir)
    };

    println!("cargo:rustc-link-search=native={}", crypto_dir);
    println!("cargo:rustc-link-lib=static=crypto");

    let ssl_dir = if cfg!(windows) {
        if cfg!(debug_assertions) {
            format!("{}/build/ssl/Debug", bssl_dir)
        } else {
            format!("{}/build/ssl/RelWithDebInfo", bssl_dir)
        }
    } else {
        format!("{}/build/ssl", bssl_dir)
    };
    println!("cargo:rustc-link-search=native={}", ssl_dir);
    println!("cargo:rustc-link-lib=static=ssl");
}
