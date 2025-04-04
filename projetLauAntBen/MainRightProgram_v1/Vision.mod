
MODULE Vision

    !Change the job name
    CONST string myjob:="MorpionVF.job";
    VAR cameratarget mycameratarget;
    !
    VAR num Xw0;
    VAR num Xw1;
    VAR num Xw2;
    VAR num Xw3;
    VAR num Xw4;
    !
    VAR num Yw0;
    VAR num Yw1;
    VAR num Yw2;
    VAR num Yw3;
    VAR num Yw4;
    !
    !
    VAR num Xb0;
    VAR num Xb1;
    VAR num Xb2;
    VAR num Xb3;
    VAR num Xb4;
    !
    VAR num Yb0;
    VAR num Yb1;
    VAR num Yb2;
    VAR num Yb3;
    VAR num Yb4;
    !  
    VAR num nDX;
    VAR num nDY;
    VAR num nFail;


    PROC LectureJeu()
        VAR num CaseTest:=-1;
        VAR num Reponse;
        VAR bool ok;

        ! Se mettre en position prise vue
        T_PriseVue;
        ! Il faut passer la caméra en mode RUN
        CamSetRunMode HandCameraR;
        !test
        ! Demande de prise de vue de la caméra
        Reponse:=17;
        WHILE Reponse=17 DO
            nFail:=1;
            WHILE nFail=1 DO
                CamReqImage HandCameraR;

                ! Attente que l'image soit calculée
                WaitTime 0.5;

                ! Vérificaiton d'avoir dvu quelque chose
                CamGetParameter HandCameraR,"PBlack.Fail"\NumVar:=nFail;

            ENDWHILE
            ! Lecture des résultats
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            CamGetParameter HandCameraR,"PBlack.Fixture.X"\NumVar:=Xb0;
            CamGetParameter HandCameraR,"PBlack.Fixture.Y"\NumVar:=Yb0;
            MatriceJeu{1,1}:=CoordToCase(Xb0,Yb0);

            CamGetParameter HandCameraR,"PBlack.Fixture1.X"\NumVar:=Xb1;
            CamGetParameter HandCameraR,"PBlack.Fixture1.Y"\NumVar:=Yb1;
            MatriceJeu{1,2}:=CoordToCase(Xb1,Yb1);

            CamGetParameter HandCameraR,"PBlack.Fixture2.X"\NumVar:=Xb2;
            CamGetParameter HandCameraR,"PBlack.Fixture2.Y"\NumVar:=Yb2;
            MatriceJeu{1,3}:=CoordToCase(Xb2,Yb2);

            CamGetParameter HandCameraR,"PBlack.Fixture3.X"\NumVar:=Xb3;
            CamGetParameter HandCameraR,"PBlack.Fixture3.Y"\NumVar:=Yb3;
            MatriceJeu{1,4}:=CoordToCase(Xb3,Yb3);

            CamGetParameter HandCameraR,"PBlack.Fixture4.X"\NumVar:=Xb4;
            CamGetParameter HandCameraR,"PBlack.Fixture4.Y"\NumVar:=Yb4;
            MatriceJeu{1,5}:=CoordToCase(Xb4,Yb4);


            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            CamGetParameter HandCameraR,"PWhite.Fixture.X"\NumVar:=Xw0;
            CamGetParameter HandCameraR,"PWhite.Fixture.Y"\NumVar:=Yw0;
            MatriceJeu{2,1}:=CoordToCase(Xw0,Yw0);

            CamGetParameter HandCameraR,"PWhite.Fixture1.X"\NumVar:=Xw1;
            CamGetParameter HandCameraR,"PWhite.Fixture1.Y"\NumVar:=Yw1;
            MatriceJeu{2,2}:=CoordToCase(Xw1,Yw1);

            CamGetParameter HandCameraR,"PWhite.Fixture2.X"\NumVar:=Xw2;
            CamGetParameter HandCameraR,"PWhite.Fixture2.Y"\NumVar:=Yw2;
            MatriceJeu{2,3}:=CoordToCase(Xw2,Yw2);

            CamGetParameter HandCameraR,"PWhite.Fixture3.X"\NumVar:=Xw3;
            CamGetParameter HandCameraR,"PWhite.Fixture3.Y"\NumVar:=Yw3;
            MatriceJeu{2,4}:=CoordToCase(Xw3,Yw3);

            CamGetParameter HandCameraR,"PWhite.Fixture4.X"\NumVar:=Xw4;
            CamGetParameter HandCameraR,"PWhite.Fixture4.Y"\NumVar:=Yw4;
            MatriceJeu{2,5}:=CoordToCase(Xw4,Yw4);

            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            ! Connection et envoie
            str_data:=Connection(IP,PORT,ValToStr(MatriceJeu));
            ok:=StrToVal(str_data,Reponse);

            IF Reponse=-1 THEN
                Reponse:=17;
            ENDIF
        ENDWHILE

        IF Reponse=-200 THEN
            TPWrite "YUMI WIN :)";
            GameFinish:=TRUE;
            WaitTime 2;
             !SocketClose socket1;
        ENDIF
        IF Reponse=-300 THEN
            TPWrite "YUMI LOSE :(";
            GameFinish:=TRUE;
            WaitTime 2;
            !SocketClose socket1;
        ENDIF
        IF Reponse=-400 THEN
            TPWrite "DRAW!";
            GameFinish:=TRUE;
            !WaitTime 2;
             !SocketClose socket1;
        ENDIF
        IF Reponse=1 OR Reponse=2 OR Reponse=3 OR Reponse=4 OR Reponse=5 OR Reponse=6 OR Reponse=7 OR Reponse=8 OR Reponse=9 THEN
            MoveIA:=Reponse;
        ENDIF
    ENDPROC

    FUNC string Connection(string Ip,num port,string message)
        !VAR num nval;
        !VAR bool ok;
        !VAR string Reception;
        !SocketClose socket1;
        !SocketCreate socket1;
        !SocketConnect socket1,Ip,port;
        SocketSend socket1\Str:=message;
        SocketReceive socket1\Str:=str_data;
        !SocketClose socket1;
        RETURN str_data;
    ERROR
        IF ERRNO=ERR_FILEOPEN THEN

            TPWrite "Erreur";
            EXIT;
        ElSEIF ERRNO=ERR_SOCK_TIMEOUT THEN
            RETRY;
        ENDIF
    ENDFUNC


    FUNC num CoordToCase(num X,num Y)
        VAR num CaseX:=-1;
        IF X=0 AND Y=0 THEN
            CaseX:=0;
        ENDIF
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        ! Case 1, 4, 7
        IF X<=-65 AND -75<=X THEN
            IF Y<=75 AND 65<=Y THEN

                CaseX:=1;
            ELSEIF Y<=-10 AND -20<=Y THEN

                CaseX:=4;
            ELSEIF Y<=-90 AND -110<=Y THEN

                CaseX:=7;
            ENDIF
        ENDIF
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        ! Case 2,5, 8
        IF X<=25 AND 15<=X THEN
            IF Y<=75 AND 65<=Y THEN
                CaseX:=2;
            ELSEIF Y<=-10 AND -20<=Y THEN
                CaseX:=5;
            ELSEIF Y<=-90 AND -110<=Y THEN
                CaseX:=8;
            ENDIF
        ENDIF
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        ! Case 3,6, 9
        IF X<=110 AND 100<=X THEN
            IF Y<=75 AND 65<=Y THEN
                CaseX:=3;
            ELSEIF Y<=-10 AND -20<=Y THEN
                CaseX:=6;
            ELSEIF Y<=-90 AND -110<=Y THEN
                CaseX:=9;
            ENDIF
        ENDIF
        RETURN CaseX;

    ENDFUNC


    PROC InitCameraAndGrip()
        VAR bool isRightHandCalibrated;
        !Change the camera name
        CamSetProgramMode HandCameraR;
        CamLoadJob HandCameraR,myjob;
        CamSetRunMode HandCameraR;
        !!!! Check and Calibrate the hand
        isRightHandCalibrated:=g_IsCalibrated();
        IF isRightHandCalibrated=FALSE THEN
            g_init;
            g_Calibrate\Jog;
        ENDIF



    ENDPROC

PROC BackupCamToCtrl(var cameradev cam,bool replaceexistingfiles)
    VAR string ctrldirname:="HOME/IV/";
    VAR dir camdirectory;
    VAR string camdirname;
    VAR string tempfilename;
    VAR string tempcamfilepath;
    VAR string tempctrlfilepath;
    
    camdirname:=CamGetName(cam)+":/";
    ctrldirname:=ctrldirname+CamGetName(cam)+"/";
    MakeDir ctrldirname;
    
    OpenDir camdirectory,camdirname;
    
    WHILE ReadDir(camdirectory,tempFileName) DO
        tempcamfilepath:=camdirname+tempfilename;
        tempctrlfilepath:=ctrldirname+tempfilename;
        CopyFile tempcamfilepath,tempctrlfilepath;
    ENDWHILE
    
    CloseDir camdirectory;
    ERROR
    IF ERRNO=ERR_FILEEXIST THEN
        IF replaceexistingfiles THEN
            RemoveFile tempctrlfilepath;
            RETRY;
        ELSE
            TRYNEXT;
        ENDIF
    ENDIF
ENDPROC


ENDMODULE