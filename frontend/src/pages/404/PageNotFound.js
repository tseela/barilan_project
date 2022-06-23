import "./PageNotFound.css"
import pic from "./404.png"

/**
 * custom page not found http 404 error
 * this page will be displayed when triyng to reach undefined url on out host
 * 
 * @returns 
 */
export default function PageNotFound() {
    return(
        <div className="page-404">
            <h1 className="header">
                <span>404</span> Page Not Found
                <br></br>
                <div className="text-404">
                    Oops... you weren't supposed to see that
                    <br></br>
                    Let us take you back to safety
                </div>
                <a className="click" href="/home">a safe place</a>
            </h1>
            <img src={pic} className="pic" alt="404 not found" />
        </div>
    )
}