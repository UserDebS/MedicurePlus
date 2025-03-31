const Error = () => {
    return ( 
        <div className="h-full w-full overflow-hidden">
            <section className="size-full flex justify-center items-center">
                <section className="h-1/2 w-1/5">
                    <strong className="inline-block font-bold text-5xl text-red-500 text-center size-full">
                        404! <br/> Page not found!
                    </strong>
                </section>
            </section>
        </div>
    );
}
 
export default Error;