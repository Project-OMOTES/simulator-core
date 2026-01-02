<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" name="test_dtk_1" description="" id="2ec3c62d-7292-4938-8930-3b539b737cc9" esdlVersion="v2507" version="7">
  <instance xsi:type="esdl:Instance" id="0a0a7858-0829-4a90-9f36-7ceed8db0438" name="Untitled instance">
    <area xsi:type="esdl:Area" id="991ab0e1-be78-4111-8e39-03592e5cc2c6" name="Untitled area">
      <asset xsi:type="esdl:HeatProducer" id="49c089de-564b-41c9-a56b-c616757aa86e" name="HeatProducer_49c0" power="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.080168451259" lon="5.17963523249716" CRS="WGS84"/>
        <port xsi:type="esdl:OutPort" id="8a6e5449-8f08-4ce4-956c-cedf9c9b8a4e" name="Out" connectedTo="e79f56b3-f362-47fa-b386-1c3645aa7e43" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:InPort" id="31cc21ee-e4db-4cd0-8493-6ddb69d3442c" name="InPort" connectedTo="661d5ff0-c971-4357-b3ff-2760666fce6a" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
      </asset>
      <asset xsi:type="esdl:HeatingDemand" id="679190ec-48e5-4b5e-8c11-633dc1513c1f" name="HeatingDemand_6791">
        <geometry xsi:type="esdl:Point" lat="52.08019481845893" lon="5.203545306045233" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="850a4675-0c79-4b3a-9562-c8ae275b88ba" name="In" connectedTo="06802302-9f65-479c-b172-ae031c8a964d" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:OutPort" id="efcf3749-bb0d-4697-8d87-e39fae365c26" name="OutPort" connectedTo="4fbb517d-f99d-494d-9da9-ce2f79f95672" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934">
          <profile xsi:type="esdl:InfluxDBProfile" measurement="WarmingUp default profiles" field="demand4_MW" host="https://profiles.warmingup.info" database="energy_profiles" filters="" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T22:00:00.000000+0000" id="ae209104-2a72-4dea-a01c-1083c2de5c76" profileType="INPUT">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:ATES" id="29bdb310-bffd-4729-be93-2f09c47ec6a9" name="ATES_29bd" maxChargeRate="11610000.0" maxDischargeRate="11610000.0" aquiferAnisotropy="4.0" aquiferMidTemperature="17.0" aquiferNetToGross="1.0" aquiferPermeability="10000.0" aquiferPorosity="0.3" aquiferThickness="45.0" aquiferTopDepth="300.0" salinity="10000.0" wellCasingSize="13.0" wellDistance="150.0">
        <geometry xsi:type="esdl:Point" lat="52.08182662637588" lon="5.187255352189122" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="40f77dd8-e494-444a-ac8f-2a3757a55e84" name="In" connectedTo="3f3f8292-76c4-4abb-b48a-85ea8ae8ad66" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:OutPort" id="85090639-f05f-4e2d-a426-223af6ac379b" name="Out" connectedTo="f913152c-5449-4087-9d72-035beb374b15" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="eac4abe3-5390-4a9d-a4dd-39a47d6615c5" name="Pipe_eac4" length="370.41">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.080827626584416" lon="5.181051807770204"/>
          <point xsi:type="esdl:Point" lat="52.08085060061373" lon="5.18647217591465"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="e79f56b3-f362-47fa-b386-1c3645aa7e43" name="In" connectedTo="8a6e5449-8f08-4ce4-956c-cedf9c9b8a4e" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:OutPort" id="bb8b4b3a-412f-46b5-987f-f50492c303ed" name="Out" carrier="497f44b0-cfe3-4c87-862c-492f9339c261" connectedTo="a2bb42dd-64b6-4145-921f-c4dc3a1e79c1"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="ee90f03d-9c11-45b8-924f-adc9f6b3fa25" name="Pipe_ee90" length="1102.19">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.08085060061373" lon="5.18647217591465"/>
          <point xsi:type="esdl:Point" lat="52.0809330937331" lon="5.202600922529884"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="eb7a116b-6863-4cd8-a8f4-40ae3b1a18fd" name="In" carrier="497f44b0-cfe3-4c87-862c-492f9339c261" connectedTo="808de90a-c5d0-40ff-a994-e25b716bbd36"/>
        <port xsi:type="esdl:OutPort" id="06802302-9f65-479c-b172-ae031c8a964d" name="Out" connectedTo="850a4675-0c79-4b3a-9562-c8ae275b88ba" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
      </asset>
      <asset xsi:type="esdl:Joint" id="fcf4d7a0-dd1e-4733-90a1-2dd01f7fabd9" name="Joint_fcf4">
        <port xsi:type="esdl:InPort" id="a2bb42dd-64b6-4145-921f-c4dc3a1e79c1" name="In" connectedTo="bb8b4b3a-412f-46b5-987f-f50492c303ed" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:OutPort" id="808de90a-c5d0-40ff-a994-e25b716bbd36" name="Out" connectedTo="eb7a116b-6863-4cd8-a8f4-40ae3b1a18fd 38a19600-5223-41c9-b2d9-4a4d386afb6f" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <geometry xsi:type="esdl:Point" lat="52.08085060061373" lon="5.18647217591465"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="f160faa6-0c5a-44b5-80f6-c85482e8988a" name="Pipe_f160" length="965.12">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.07985204364499" lon="5.2026438490533"/>
          <point xsi:type="esdl:Point" lat="52.07977562862388" lon="5.188521308358817"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="4fbb517d-f99d-494d-9da9-ce2f79f95672" name="In" connectedTo="efcf3749-bb0d-4697-8d87-e39fae365c26" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
        <port xsi:type="esdl:OutPort" id="7311dd47-7913-40ae-8cb4-e41044b82613" name="Out" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934" connectedTo="a9c6664d-703b-43d0-9e40-c96f818786eb"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="f7b9d0ce-a67b-43a6-b917-b8b14b43e1fd" name="Pipe_f7b9" length="501.65">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.07977562862388" lon="5.188521308358817"/>
          <point xsi:type="esdl:Point" lat="52.07974657394189" lon="5.181180587340451"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="2b6c670d-5772-4c09-878e-02ef082daa27" name="In" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934" connectedTo="7b073925-a8e0-4fa9-b1e6-cb6ef3ed6fed"/>
        <port xsi:type="esdl:OutPort" id="661d5ff0-c971-4357-b3ff-2760666fce6a" name="Out" connectedTo="31cc21ee-e4db-4cd0-8493-6ddb69d3442c" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
      </asset>
      <asset xsi:type="esdl:Joint" id="f16f1a52-15f1-4e08-85c0-c9423c00b1dd" name="Joint_f16f">
        <port xsi:type="esdl:InPort" id="a9c6664d-703b-43d0-9e40-c96f818786eb" name="In" connectedTo="7311dd47-7913-40ae-8cb4-e41044b82613 a0fb84d7-9415-4d54-8e0c-e4206818c7dd" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
        <port xsi:type="esdl:OutPort" id="7b073925-a8e0-4fa9-b1e6-cb6ef3ed6fed" name="Out" connectedTo="2b6c670d-5772-4c09-878e-02ef082daa27" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
        <geometry xsi:type="esdl:Point" lat="52.07977562862388" lon="5.188521308358817"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="3319e25a-9ccd-44bf-9c13-78c556237ccd" name="Pipe_3319" length="91.7">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.08098234825138" lon="5.186450721000124"/>
          <point xsi:type="esdl:Point" lat="52.08180669330172" lon="5.1864399925580305"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="38a19600-5223-41c9-b2d9-4a4d386afb6f" name="In" connectedTo="808de90a-c5d0-40ff-a994-e25b716bbd36" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:OutPort" id="3f3f8292-76c4-4abb-b48a-85ea8ae8ad66" name="Out" connectedTo="40f77dd8-e494-444a-ac8f-2a3757a55e84" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="b38a0db2-adf1-4d17-a0fb-4850f94e039f" name="Pipe_b38a" length="193.6">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.08178031449592" lon="5.188231642391404"/>
          <point xsi:type="esdl:Point" lat="52.08003927884225" lon="5.188285284601997"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="f913152c-5449-4087-9d72-035beb374b15" name="In" connectedTo="85090639-f05f-4e2d-a426-223af6ac379b" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
        <port xsi:type="esdl:OutPort" id="a0fb84d7-9415-4d54-8e0c-e4206818c7dd" name="Out" connectedTo="a9c6664d-703b-43d0-9e40-c96f818786eb" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
      </asset>
    </area>
  </instance>
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="6955a3da-0f5d-4e9c-881d-685bb5f1a8c0">
    <carriers xsi:type="esdl:Carriers" id="6e43055a-a009-462f-8f29-91ade19b0a8c">
      <carrier xsi:type="esdl:HeatCommodity" id="497f44b0-cfe3-4c87-862c-492f9339c261" name="Supply" supplyTemperature="80.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="b34bc6ff-0f30-48d9-8604-9e9db1e34934" name="Return" returnTemperature="50.0"/>
    </carriers>
    <quantityAndUnits xsi:type="esdl:QuantityAndUnits" id="774562e8-aec5-4ff4-9efc-63bb45437f10">
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="12c481c0-f81e-49b6-9767-90457684d24a" description="Energy in kWh" physicalQuantity="ENERGY" multiplier="KILO" unit="WATTHOUR"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="93aa23ea-4c5d-4969-97d4-2a4b2720e523" description="Energy in MWh" physicalQuantity="ENERGY" multiplier="MEGA" unit="WATTHOUR"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="e9405fc8-5e57-4df5-8584-4babee7cdf1b" description="Power in MW" physicalQuantity="POWER" multiplier="MEGA" unit="WATT"/>
    </quantityAndUnits>
  </energySystemInformation>
</esdl:EnergySystem>
