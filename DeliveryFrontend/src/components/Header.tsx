const Header = () => {
    return ( 
        <header className="h-14 shadow-md bg-white">
            <div className="h-full w-full">
                <img src={(window.location.origin + '/logo.png')} alt="Logo" height={"3.5em"} className="h-full" />
            </div>
        </header>
    );
}
 
export default Header;