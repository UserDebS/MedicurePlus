import { Outlet } from "react-router-dom";
import Header from "./Header";
import { Toaster } from "sonner";

const Layout = () => {
    return ( 
        <div className="h-lvh w-lvw">
            <Toaster />
            <Header />
            <main className="h-[calc(100%-3.5em)]">
                <Outlet />
            </main>
        </div>
    );
}
 
export default Layout;