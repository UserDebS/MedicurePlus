import Header from "./Header";
import { Outlet } from "react-router";
const Layout = () => {
    const currentPath : string = window.location.pathname
    return ( 
        <div className="h-lvh w-lvw overflow-hidden">
            <Header />
            <main className="h-[calc(100lvh-3.5rem)] overflow-y-auto">
                <Outlet/>
            </main>
        </div>
     );
}
 
export default Layout;