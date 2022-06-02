import "./Forbidden.css"
import pic from "./naughty.jpg"

export default function Forbidden() {
    return(
        <div className="page-forbidden">
            <div className="body-forbidden">
                <h1 className="header">
                    <span>403</span> Forbidden!
                    <br></br>
                    <div className="text">
                        Well... It appears that someone is on the naughty list this year...
                        <br></br>
                        Maybe you got here by mistake? Try to <a href="/login">login</a> if you are not connected yet.
                    </div>
                </h1>
                <img src={pic} className="pic" alt="404 not found" />
            </div>
        </div>
    )
}