const Navbar = () => {
    return (
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container-fluid d-flex justify-content-between">
                <a className="navbar-brand" href="/">System zarządzania wnioskami</a>
                <a className="navbar-brand" href="/login">Login</a>
            </div>
        </nav>
    );
}

export default Navbar;