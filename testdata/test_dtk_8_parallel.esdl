<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" name="test_dtk_1" description="" id="2ec3c62d-7292-4938-8930-3b539b737cc9" esdlVersion="v2507" version="9">
  <instance xsi:type="esdl:Instance" id="0a0a7858-0829-4a90-9f36-7ceed8db0438" name="Untitled instance">
    <area xsi:type="esdl:Area" id="991ab0e1-be78-4111-8e39-03592e5cc2c6" name="Untitled area">
      <asset xsi:type="esdl:HeatProducer" id="49c089de-564b-41c9-a56b-c616757aa86e" name="HeatProducer_49c0" power="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.080168451259" lon="5.17963523249716" CRS="WGS84"/>
        <port xsi:type="esdl:OutPort" id="8a6e5449-8f08-4ce4-956c-cedf9c9b8a4e" name="Out" connectedTo="4eed84a0-5bba-4a34-8374-4fe4c82c91e4" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:InPort" id="31cc21ee-e4db-4cd0-8493-6ddb69d3442c" name="InPort" connectedTo="1edce403-4778-45b3-8e06-246a6f44857c" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
      </asset>
      <asset xsi:type="esdl:HeatingDemand" id="679190ec-48e5-4b5e-8c11-633dc1513c1f" name="HeatingDemand_6791" power="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.08019481845893" lon="5.203545306045233" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="850a4675-0c79-4b3a-9562-c8ae275b88ba" name="In" connectedTo="2f79d5b2-9a60-4a1d-aab9-034937d9f7bf" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf"/>
        <port xsi:type="esdl:OutPort" id="efcf3749-bb0d-4697-8d87-e39fae365c26" name="OutPort" connectedTo="0484020b-3fae-48d1-89b5-d37bc1095cb4" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11">
          <profile xsi:type="esdl:InfluxDBProfile" measurement="WarmingUp default profiles" field="demand4_MW" host="https://profiles.warmingup.info" database="energy_profiles" filters="" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T22:00:00.000000+0000" id="ae209104-2a72-4dea-a01c-1083c2de5c76" profileType="INPUT">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:HeatExchange" id="db270abe-fe5b-45e5-a9a3-ef3bef61b72b" name="HeatExchange_db27" capacity="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.08017726075351" lon="5.192096279200813" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="b40c0fb5-5e07-4568-a13c-7549d0bb3913" name="PrimIn" connectedTo="bd6a7f01-3755-473b-8a44-0e19ff07f05a" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:OutPort" id="8c109b7c-61f9-4913-a23b-7490f0296054" name="SecOut" connectedTo="8d79c71e-8c27-4c6e-afa2-eeda757964bb" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf"/>
        <port xsi:type="esdl:InPort" id="fafdd706-b147-4d9a-a04f-c3c7bda8e1a2" name="SecIn" connectedTo="2fa55afc-fa8c-4ce6-8ea4-c76de866cdd5" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11"/>
        <port xsi:type="esdl:OutPort" id="5efae14e-42f7-498f-b768-3cf9437f5710" name="PrimOut" connectedTo="54a7a58c-340d-4d8a-85d5-4e83de250b32" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
      </asset>
      <asset xsi:type="esdl:HeatExchange" id="30f0d155-ad4b-48e5-9740-9b8fb1e4980b" name="HeatExchange_30f0">
        <geometry xsi:type="esdl:Point" lat="52.07812293196015" lon="5.191969766880314" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="8e3312d1-30c7-4680-b15d-e70677511829" name="PrimIn" connectedTo="875da567-6aeb-4356-892d-1a527a0d9f26" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:OutPort" id="74b2b27c-481b-4361-98f3-d71adf146d55" name="PrimOut" connectedTo="2f11650f-7342-47c3-bfa3-47634e6d2b52" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
        <port xsi:type="esdl:InPort" id="789b9b18-25d1-47ec-ad33-8bf2cf8ef72e" name="SecIn" connectedTo="08f59a04-36c0-4db5-8884-d6f4fd2af2b9" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11"/>
        <port xsi:type="esdl:OutPort" id="a275ef97-bb89-4710-9916-46a066b3c9ec" name="SecOut" connectedTo="787a9c56-4a0f-49c8-aa8e-5965374839cc" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="f6ddbbb3-a431-4cf0-88d3-20aceb473a2f" name="Pipe_f6dd" length="230.2">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.08048282249382" lon="5.189136113270797"/>
          <point xsi:type="esdl:Point" lat="52.078412963275355" lon="5.189114650009068"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="3d2a9d20-75e3-4fd2-ab95-5c92674a90d8" name="In" connectedTo="345d8c43-5e9e-4ca3-bd40-667aef2bd5c5" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:OutPort" id="875da567-6aeb-4356-892d-1a527a0d9f26" name="Out" connectedTo="8e3312d1-30c7-4680-b15d-e70677511829" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="1fc2dcdc-7b4c-4a04-9bdb-c78393afca28" name="Pipe_1fc2" length="214.1">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.07754280271879" lon="5.1901019600478735"/>
          <point xsi:type="esdl:Point" lat="52.079467680603024" lon="5.190166349833017"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="2f11650f-7342-47c3-bfa3-47634e6d2b52" name="In" connectedTo="74b2b27c-481b-4361-98f3-d71adf146d55" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
        <port xsi:type="esdl:OutPort" id="da8e8fcd-8259-405e-b1ac-8f931477c0bf" name="Out" connectedTo="0cf44e41-7115-4e1b-b677-04816a78d770" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="2f470d58-f682-4128-b440-f1d373304026" name="Pipe_2f47" length="249.2">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.07948086441191" lon="5.1952102163355205"/>
          <point xsi:type="esdl:Point" lat="52.077239560963555" lon="5.195231679597248"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="6468a4d9-43c9-4d34-9952-281b3a9028a7" name="In" connectedTo="60bee5c8-0078-4d81-97cc-f7b066c8e196" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11"/>
        <port xsi:type="esdl:OutPort" id="08f59a04-36c0-4db5-8884-d6f4fd2af2b9" name="Out" connectedTo="789b9b18-25d1-47ec-ad33-8bf2cf8ef72e" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="973d452c-2a4f-4c2d-af91-a30b7d611557" name="Pipe_973d" length="212.6">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.078557988385676" lon="5.193621934968774"/>
          <point xsi:type="esdl:Point" lat="52.08046963898088" lon="5.193621934968774"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="787a9c56-4a0f-49c8-aa8e-5965374839cc" name="In" connectedTo="a275ef97-bb89-4710-9916-46a066b3c9ec" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf"/>
        <port xsi:type="esdl:OutPort" id="28985591-87d3-496b-ad61-e7a53a57d176" name="Out" connectedTo="f6fef914-bb7b-44ab-9b7a-ad3d0f3a0f46" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="9b3d7f93-7645-4b64-8176-bd238bf98e42" name="Pipe_9b3d" length="584.44">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.080704870213225" lon="5.180552471544395"/>
          <point xsi:type="esdl:Point" lat="52.08071931736118" lon="5.189104984819419"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="4eed84a0-5bba-4a34-8374-4fe4c82c91e4" name="In" connectedTo="8a6e5449-8f08-4ce4-956c-cedf9c9b8a4e" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:OutPort" id="00b2e47c-2839-4eb3-94a0-539543925fff" name="Out" carrier="497f44b0-cfe3-4c87-862c-492f9339c261" connectedTo="1a185cd1-5e56-4595-aa99-1e839fcb35ec"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="65b01b4c-726d-474c-89cb-f8b9e3bd050f" name="Pipe_65b0" length="141.36">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.08071931736118" lon="5.189104984819419"/>
          <point xsi:type="esdl:Point" lat="52.08071805993588" lon="5.1911736292393815"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="01e37021-fdfd-4c41-a8c9-abd6def80c65" name="In" carrier="497f44b0-cfe3-4c87-862c-492f9339c261" connectedTo="345d8c43-5e9e-4ca3-bd40-667aef2bd5c5"/>
        <port xsi:type="esdl:OutPort" id="bd6a7f01-3755-473b-8a44-0e19ff07f05a" name="Out" connectedTo="b40c0fb5-5e07-4568-a13c-7549d0bb3913" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
      </asset>
      <asset xsi:type="esdl:Joint" id="082774be-91aa-4e38-ba5d-eeaac71baf59" name="Joint_0827">
        <port xsi:type="esdl:InPort" id="1a185cd1-5e56-4595-aa99-1e839fcb35ec" name="In" connectedTo="00b2e47c-2839-4eb3-94a0-539543925fff" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:OutPort" id="345d8c43-5e9e-4ca3-bd40-667aef2bd5c5" name="Out" connectedTo="01e37021-fdfd-4c41-a8c9-abd6def80c65 3d2a9d20-75e3-4fd2-ab95-5c92674a90d8" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <geometry xsi:type="esdl:Point" lat="52.08071931736118" lon="5.189104984819419"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="9d522bc4-da4d-4cb0-b7b7-7e58aef2c8cf" name="Pipe_9d52" length="72.8">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.07966286980711" lon="5.191216543007839"/>
          <point xsi:type="esdl:Point" lat="52.07966792554655" lon="5.190151318827897"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="54a7a58c-340d-4d8a-85d5-4e83de250b32" name="In" connectedTo="5efae14e-42f7-498f-b768-3cf9437f5710" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
        <port xsi:type="esdl:OutPort" id="3b007d69-9010-4c17-8a85-da3079af4571" name="Out" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934" connectedTo="8e394a03-f356-4646-abd4-7158c665b7da"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="0a762af1-a9c6-481b-a2c1-b904c3e3235d" name="Pipe_0a76" length="657.49">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.07966792554655" lon="5.190151318827897"/>
          <point xsi:type="esdl:Point" lat="52.07958372954184" lon="5.180531014660167"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="0cf44e41-7115-4e1b-b677-04816a78d770" name="In" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934" connectedTo="fc085f97-2d30-4464-95cc-52d79549be9c da8e8fcd-8259-405e-b1ac-8f931477c0bf"/>
        <port xsi:type="esdl:OutPort" id="1edce403-4778-45b3-8e06-246a6f44857c" name="Out" connectedTo="31cc21ee-e4db-4cd0-8493-6ddb69d3442c" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
      </asset>
      <asset xsi:type="esdl:Joint" id="a0498989-6c8e-4f74-91cc-709fe266c913" name="Joint_a049">
        <port xsi:type="esdl:InPort" id="8e394a03-f356-4646-abd4-7158c665b7da" name="In" connectedTo="3b007d69-9010-4c17-8a85-da3079af4571" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
        <port xsi:type="esdl:OutPort" id="fc085f97-2d30-4464-95cc-52d79549be9c" name="Out" connectedTo="0cf44e41-7115-4e1b-b677-04816a78d770" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
        <geometry xsi:type="esdl:Point" lat="52.07966792554655" lon="5.190151318827897"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="802b0d8c-7224-4118-bbc4-9f262a936190" name="Pipe_802b" length="48.58">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.080704870213225" lon="5.192890179977971"/>
          <point xsi:type="esdl:Point" lat="52.08071937408159" lon="5.193600722067578"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="8d79c71e-8c27-4c6e-afa2-eeda757964bb" name="In" connectedTo="8c109b7c-61f9-4913-a23b-7490f0296054" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf"/>
        <port xsi:type="esdl:OutPort" id="82d8932c-d07b-4530-a046-40edebadc5ab" name="Out" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf" connectedTo="f6fef914-bb7b-44ab-9b7a-ad3d0f3a0f46"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="48959892-58b4-4987-bf5a-85b00112cdff" name="Pipe_4895" length="634.75">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.08071937408159" lon="5.193600722067578"/>
          <point xsi:type="esdl:Point" lat="52.0807708187875" lon="5.202889088030225"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="a1ddd523-6f89-4e4e-9138-231461fc3cea" name="In" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf" connectedTo="0bfc04f8-d7fa-446a-9537-d6fe551c38e9"/>
        <port xsi:type="esdl:OutPort" id="2f79d5b2-9a60-4a1d-aab9-034937d9f7bf" name="Out" connectedTo="850a4675-0c79-4b3a-9562-c8ae275b88ba" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf"/>
      </asset>
      <asset xsi:type="esdl:Joint" id="96e13613-bd7a-4a4e-b32d-9f041aa18117" name="Joint_96e1">
        <port xsi:type="esdl:InPort" id="f6fef914-bb7b-44ab-9b7a-ad3d0f3a0f46" name="In" connectedTo="82d8932c-d07b-4530-a046-40edebadc5ab 28985591-87d3-496b-ad61-e7a53a57d176" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf"/>
        <port xsi:type="esdl:OutPort" id="0bfc04f8-d7fa-446a-9537-d6fe551c38e9" name="Out" connectedTo="a1ddd523-6f89-4e4e-9138-231461fc3cea" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf"/>
        <geometry xsi:type="esdl:Point" lat="52.08071937408159" lon="5.193600722067578"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="c4ea8f0a-e68b-4a45-bb0c-52a2dce9627b" name="Pipe_c4ea" length="540.19">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.07972881992095" lon="5.2031036568725195"/>
          <point xsi:type="esdl:Point" lat="52.07965479851469" lon="5.195199735065189"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="0484020b-3fae-48d1-89b5-d37bc1095cb4" name="In" connectedTo="efcf3749-bb0d-4697-8d87-e39fae365c26" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11"/>
        <port xsi:type="esdl:OutPort" id="50e46ec6-95bc-4f69-999d-6726f8da9e22" name="Out" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11" connectedTo="eded0b4c-c532-4227-835b-f5077bd334f5"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="c0428ed2-8ea8-4754-bba6-5398c0a500c0" name="Pipe_c042" length="154.93">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.07965479851469" lon="5.195199735065189"/>
          <point xsi:type="esdl:Point" lat="52.07962329969199" lon="5.19293309374643"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="26f20a71-4f76-4bb5-aba8-04c478ffe0d0" name="In" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11" connectedTo="60bee5c8-0078-4d81-97cc-f7b066c8e196"/>
        <port xsi:type="esdl:OutPort" id="2fa55afc-fa8c-4ce6-8ea4-c76de866cdd5" name="Out" connectedTo="fafdd706-b147-4d9a-a04f-c3c7bda8e1a2" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11"/>
      </asset>
      <asset xsi:type="esdl:Joint" id="aa37de9a-568e-4336-95f6-70497d29c190" name="Joint_aa37">
        <port xsi:type="esdl:InPort" id="eded0b4c-c532-4227-835b-f5077bd334f5" name="In" connectedTo="50e46ec6-95bc-4f69-999d-6726f8da9e22" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11"/>
        <port xsi:type="esdl:OutPort" id="60bee5c8-0078-4d81-97cc-f7b066c8e196" name="Out" connectedTo="26f20a71-4f76-4bb5-aba8-04c478ffe0d0 6468a4d9-43c9-4d34-9952-281b3a9028a7" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11"/>
        <geometry xsi:type="esdl:Point" lat="52.07965479851469" lon="5.195199735065189"/>
      </asset>
    </area>
  </instance>
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="6955a3da-0f5d-4e9c-881d-685bb5f1a8c0">
    <carriers xsi:type="esdl:Carriers" id="6e43055a-a009-462f-8f29-91ade19b0a8c">
      <carrier xsi:type="esdl:HeatCommodity" id="497f44b0-cfe3-4c87-862c-492f9339c261" name="Supply" supplyTemperature="80.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="b34bc6ff-0f30-48d9-8604-9e9db1e34934" name="Return" returnTemperature="50.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="baeed7a3-22e7-43b4-ad3b-837aa0634daf" name="SecSupply" returnTemperature="75.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="7cd930ee-a18e-4783-a9cf-6d64bf298a11" name="SecReturn" returnTemperature="55.0"/>
    </carriers>
    <quantityAndUnits xsi:type="esdl:QuantityAndUnits" id="774562e8-aec5-4ff4-9efc-63bb45437f10">
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="12c481c0-f81e-49b6-9767-90457684d24a" description="Energy in kWh" physicalQuantity="ENERGY" multiplier="KILO" unit="WATTHOUR"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="93aa23ea-4c5d-4969-97d4-2a4b2720e523" description="Energy in MWh" physicalQuantity="ENERGY" multiplier="MEGA" unit="WATTHOUR"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="e9405fc8-5e57-4df5-8584-4babee7cdf1b" description="Power in MW" physicalQuantity="POWER" multiplier="MEGA" unit="WATT"/>
    </quantityAndUnits>
  </energySystemInformation>
</esdl:EnergySystem>
