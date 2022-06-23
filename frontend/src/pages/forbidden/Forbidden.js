import "./Forbidden.css"
import pic from "./naughty.jpg"

/**
 * forbidden access page error 403
 * appears when trying to view/edit a trip the user doesn't own (or when the user is not connected)
 * 
 * @returns 
 */
export default function Forbidden() {
    return(
        <div className="page-forbidden">
            <div className="body-forbidden">
                <h1 className="header">
                    <span>403</span> Forbidden!
                    <br></br>
                    <div className="text-forbidden">
                        Well... It appears that someone is on the naughty list this year...
                        <br></br>
                        Maybe you got here by mistake? Try to <a href="/login">login</a> if you are not connected yet.
                    </div>
                    <div className="more-text">
                        If you are connected, know that you are getting this message because you are trying to view a trip of another user.
                    </div>
                </h1>
                <img src={pic} className="pic" alt="404 not found" />
            </div>
        </div>
    )
}