import React from "react";
import {Panel ,Table,PanelGroup} from "rsuite"
import "rsuite/dist/rsuite.min.css";
import group from "../data/group.json"

export default function MainPage(){
    return(
        <div>
        <PanelGroup accordion bordered>
            <Panel header="COMP90024 Assignment2 - Team 03" expanded shaded>
                <p style={{fontSize:18}}>
                    The goal of this project is to build our system on UniMelb Research Cloud(MRC), hence we used ansible to deploy our web application in an automatic way. Ansible is an open-source tool for application-deployment which can enable infrastructure as code. It is a simple but powerful automation for multi-platform computer support. Ansible is mainly focused on IT professionals, who use it to deploy application, update server and cloud provisioning. Because of the fact that Ansible does not need any agent software and additional security infrastructure, it is convenient to deploy. Section 3.3 shows more details.
                </p>
                <br/>
                <p> Github Link : https://github.com/Yanbei-Jiang/COMP90024_Ass2</p>
            </Panel>
            <Panel header="Group Info" expanded shaded bodyFill>
                <Table
                height={400}
                data={group}
                onRowClick={data => {
                    console.log(data);
                }}
                >
                    <Table.Column width={200} fixed>
                        <Table.HeaderCell>Student ID</Table.HeaderCell>
                        <Table.Cell dataKey="id" />
                    </Table.Column>

                    <Table.Column width={200} fixed>
                        <Table.HeaderCell>First Name</Table.HeaderCell>
                        <Table.Cell dataKey="firstName" />
                    </Table.Column>

                    <Table.Column width={200}>
                        <Table.HeaderCell>Last Name</Table.HeaderCell>
                        <Table.Cell dataKey="lastName" />
                    </Table.Column>

                    <Table.Column width={300}>
                        <Table.HeaderCell>Email</Table.HeaderCell>
                        <Table.Cell dataKey="email" />
                    </Table.Column>

                    <Table.Column width={300}>
                        <Table.HeaderCell>Jobs</Table.HeaderCell>
                        <Table.Cell dataKey="job" />
                    </Table.Column>
                </Table>
            </Panel>
        </PanelGroup>
    </div>
    )
}